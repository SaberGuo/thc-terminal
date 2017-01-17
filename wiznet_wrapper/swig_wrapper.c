//
// Created by saber on 2016/12/14.
//

#include "wizchip_conf.h"
#include "commons.h"
#include "socket.h"
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "swig_wrapper.h"

#include "rpi.h"

void init_hardware(){
    bcm2835_initlize();
    reg_wizchip_cs_cbfunc(wizchip_cs_sel, wizchip_cs_desel);
    reg_wizchip_spi_cbfunc(rpi_spi_readbyte, rpi_spi_writebyte);
    reg_wizchip_spiburst_cbfunc(rpi_spi_readburst, rpi_spi_writeburst);
}

void init_conf(char *ip, char *mask, char *gateway){
    wiz_NetInfo mWIZNETINFO= {.mac = {0x00, 0x08, 0xdc, 0xab, 0xcd, 0xef},
        .ip = {192, 168, 1, 199},
        .sn = {255, 255, 255, 0},
        .gw = {192, 168, 1, 1},
        .dns = {8, 8, 8, 8},
        .dhcp = NETINFO_STATIC };;

    if(WIZNET_ERROR == str_to_netarray(mWIZNETINFO.ip,4,ip))
    {
        return;
    }
    if(WIZNET_ERROR == str_to_netarray(mWIZNETINFO.sn,4,mask))
    {
        return;
    }
    if(WIZNET_ERROR == str_to_netarray(mWIZNETINFO.gw,4,gateway))
    {
        return;
    }
    ctlnetwork(CN_SET_NETINFO, (void *)&mWIZNETINFO);
#ifdef _WIZNET_DEBUG_
    ctlnetwork(CN_GET_NETINFO, (void *)&mWIZNETINFO);
    printf("mac: 0x%02X-0x%02X-0x%02X-0x%02X-0x%02X-0x%02X\n",
           mWIZNETINFO.mac[0], mWIZNETINFO.mac[1], mWIZNETINFO.mac[2], mWIZNETINFO.mac[3], mWIZNETINFO.mac[4], mWIZNETINFO.mac[5]);
    printf("ip: %d.%d.%d.%d\n", mWIZNETINFO.ip[0],mWIZNETINFO.ip[1],mWIZNETINFO.ip[2],mWIZNETINFO.ip[3]);
    printf("sn: %d.%d.%d.%d\n", mWIZNETINFO.sn[0],mWIZNETINFO.sn[1],mWIZNETINFO.sn[2],mWIZNETINFO.sn[3]);
    printf("gw: %d.%d.%d.%d\n", mWIZNETINFO.gw[0],mWIZNETINFO.gw[1],mWIZNETINFO.gw[2],mWIZNETINFO.gw[3]);
#endif
    return;
}

char tcpc_buf[DATA_BUF_SIZE] = {0};
int tcpc_buf_size = 0;
int loopback_tcpc(int sn, char *ip, int port)
{
        printf("loopback_tcpc:ip-%s\n",ip );
	uint8_t tcpc_ip[4]={0};
	int tcpc_port = 1000;
	str_to_netarray(tcpc_ip, 4, ip);
        //tcpc_ip[0] = 192;
        //tcpc_ip[1] = 168;
        //tcpc_ip[2] = 1;
        //tcpc_ip[3] = 100;
    tcpc_port = port;
    int32_t ret; // return value for SOCK_ERRORs
	uint16_t size = 0, sentsize=0;
    // Destination (TCP Server) IP info (will be connected)
    // >> loopback_tcpc() function parameter
    // >> Ex)
    //	uint8_t destip[4] = 	{192, 168, 0, 214};
    //	uint16_t destport = 	5000;

    // Port number for TCP client (will be increased)
    uint16_t any_port = 	50000;

    // Socket Status Transitions
    // Check the W5500 Socket n status register (Sn_SR, The 'Sn_SR' controlled by Sn_CR command or Packet send/recv status)
    switch(getSn_SR(sn))
    {
        case SOCK_ESTABLISHED :
            if(getSn_IR(sn) & Sn_IR_CON)	// Socket n interrupt register mask; TCP CON interrupt = connection with peer is successful
            {
#ifdef _LOOPBACK_DEBUG_
                printf("%d:Connected to - %d.%d.%d.%d : %d\r\n",sn, tcpc_ip[0], tcpc_ip[1], tcpc_ip[2], tcpc_ip[3], tcpc_port);
#endif
                setSn_IR(sn, Sn_IR_CON);  // this interrupt should be write the bit cleared to '1'
            }

            //////////////////////////////////////////////////////////////////////////////////////////////
            // Data Transaction Parts; Handle the [data receive and send] process
            //////////////////////////////////////////////////////////////////////////////////////////////
            if((size = getSn_RX_RSR(sn)) > 0) // Sn_RX_RSR: Socket n Received Size Register, Receiving data length
            {
                if(size > DATA_BUF_SIZE) size = DATA_BUF_SIZE; // DATA_BUF_SIZE means user defined buffer size (array)
                ret = srecv(sn, tcpc_buf, size); // Data Receive process (H/W Rx socket buffer -> User's buffer)

                if(ret <= 0) return ret; // If the received data length <= 0, receive failed and process end
                sentsize = 0;
				tcpc_buf_size = size;
				return 2; //got recv data

                // Data sentsize control
            }
            return 3; // got ready for send
            //////////////////////////////////////////////////////////////////////////////////////////////
            break;

        case SOCK_CLOSE_WAIT :
#ifdef _LOOPBACK_DEBUG_
            //printf("%d:CloseWait\r\n",sn);
#endif
            if((ret=sdisconnect(sn)) != SOCK_OK) return ret;
#ifdef _LOOPBACK_DEBUG_
            printf("%d:Socket Closed\r\n", sn);
#endif
            break;

        case SOCK_INIT :
#ifdef _LOOPBACK_DEBUG_
            printf("%d:Try to connect to the %d.%d.%d.%d : %d\r\n", sn, tcpc_ip[0], tcpc_ip[1], tcpc_ip[2], tcpc_ip[3], tcpc_port);
         printf("%d: socke mode 0x%02x\n", sn, getSn_MR(sn));
#endif
            if( (ret = sconnect(sn, tcpc_ip, tcpc_port)) != SOCK_OK) return ret;	//	Try to TCP connect to the TCP server (destination)
            break;

        case SOCK_CLOSED:
            printf("close the socket %d\n", sn); 
            sclose(sn);
            if((ret=ssocket(sn, Sn_MR_TCP, any_port++, 0x00)) != sn) return ret; // TCP socket open with 'any_port' port number
#ifdef _LOOPBACK_DEBUG_
        printf("%d:TCP client loopback start\r\n",sn);
        printf("%d:Socket opened\r\n",sn);
#endif
            break;
        default:
            break;
    }
	ret = 1;
    return ret;
}

char tcps_buf[DATA_BUF_SIZE] = {0};
int tcps_buf_size = 0;
int loopback_tcps(int sn, int port)
{
   int32_t ret;
   uint16_t size = 0, sentsize=0;

#ifdef _LOOPBACK_DEBUG_
   uint8_t destip[4];
   uint16_t destport;
#endif

   switch(getSn_SR(sn))
   {
      case SOCK_ESTABLISHED :
         if(getSn_IR(sn) & Sn_IR_CON)
         {
#ifdef _LOOPBACK_DEBUG_
			getSn_DIPR(sn, destip);
			destport = getSn_DPORT(sn);

			printf("%d:Connected - %d.%d.%d.%d : %d\r\n",sn, destip[0], destip[1], destip[2], destip[3], destport);
#endif
			setSn_IR(sn,Sn_IR_CON);
         }
		 if((size = getSn_RX_RSR(sn)) > 0) // Don't need to check SOCKERR_BUSY because it doesn't not occur.
         {
			if(size > DATA_BUF_SIZE) size = DATA_BUF_SIZE;
			ret = srecv(sn, tcps_buf, size);

			if(ret <= 0) return ret;      // check SOCKERR_BUSY & SOCKERR_XXX. For showing the occurrence of SOCKERR_BUSY.
			sentsize = 0;
			tcps_buf_size = size;
			return 2;

         }
         return 3; //got ready for send
         break;
      case SOCK_CLOSE_WAIT :
#ifdef _LOOPBACK_DEBUG_
         //printf("%d:CloseWait\r\n",sn);
#endif
         if((ret = sdisconnect(sn)) != SOCK_OK) return ret;
#ifdef _LOOPBACK_DEBUG_
         printf("%d:Socket Closed\r\n", sn);
#endif
         break;
      case SOCK_INIT :
#ifdef _LOOPBACK_DEBUG_
    	 printf("%d:Listen, TCP server loopback, port [%d]\r\n", sn, port);
#endif
         if( (ret = slisten(sn)) != SOCK_OK) return ret;
         break;
      case SOCK_CLOSED:
#ifdef _LOOPBACK_DEBUG_
         //printf("%d:TCP server loopback start\r\n",sn);
#endif
         if((ret = ssocket(sn, Sn_MR_TCP, port, 0x00)) != sn) return ret;
#ifdef _LOOPBACK_DEBUG_
         //printf("%d:Socket opened\r\n",sn);
#endif
         break;
      default:
         break;
   }
   return 1;
}

void tcpc_recv(char *res, size_t *res_size){
    //printf("%s", tcpc_buf);
	*res_size = tcpc_buf_size;
	size_t i=0;
	for(;i<*res_size;i++ ){
        *res++ = tcpc_buf[i];}
	*res = 0;
}

void tcps_recv(char *res, size_t *res_size){
    *res_size = tcps_buf_size;
	size_t i=0;
	for(;i<*res_size;i++ ){
        *res++ = tcps_buf[i];}
	*res = 0;
}

int socket_send(int sn, char *buf, size_t buf_size){
    return ssend(sn, buf, buf_size);
}

int socket_close(int sn){
    return sclose(sn);
}