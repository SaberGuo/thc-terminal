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
#include "dns.h"
#include "rpi.h"

uint8_t dns[4] = {192,168,1,1};
uint8_t dns_bk[4] = {210,2,4,8};


void init_hardware(){
    bcm2835_initlize();
    reg_wizchip_cs_cbfunc(wizchip_cs_sel, wizchip_cs_desel);
    reg_wizchip_spi_cbfunc(rpi_spi_readbyte, rpi_spi_writebyte);
    reg_wizchip_spiburst_cbfunc(rpi_spi_readburst, rpi_spi_writeburst);
}

void init_conf(char *ip, char *mask, char *gateway){
    ctlwizchip(CW_RESET_WIZCHIP,NULL);
    uint8_t memsize[2][8] = { { 2, 2, 2, 2, 2, 2, 2, 2 }, { 2, 2, 2, 2, 2, 2, 2, 2 } };
    if (ctlwizchip(CW_INIT_WIZCHIP, (void*) memsize) == -1) {
		printf("WIZCHIP Initialized fail.\r\n");
		while (1);
	}
    wiz_NetInfo mWIZNETINFO= {.mac = {0x00, 0x08, 0xDC, 0x44, 0xef, 0x66},
        .ip = {192, 168, 1, 105},
        .sn = {255, 255, 255, 0},
        .gw = {192, 168, 1, 1},
        .dns = {192,168,1,1},
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
    char tmpip[20] = {0};
    strcat(tmpip, ip);
    uint8_t tcpc_ip[4]={0};
    int tcpc_port = 1000;
	str_to_netarray(tcpc_ip, 4, tmpip);

    tcpc_port = port;
    int32_t ret; // return value for SOCK_ERRORs
	uint16_t size = 0;
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
				tcpc_buf_size = size;
				return 2; //got recv data

                // Data sentsize control
            }
            return 3; // got ready for send
            //////////////////////////////////////////////////////////////////////////////////////////////
            break;

        case SOCK_CLOSE_WAIT :
#ifdef _LOOPBACK_DEBUG_
            printf("%d:CloseWait\r\n",sn);
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
			while(size != sentsize)
			{
				ret = send(sn, tcps_buf+sentsize, size-sentsize);
				if(ret < 0)
				{
					close(sn);
					return ret;
				}
				sentsize += ret; // Don't care SOCKERR_BUSY, because it is zero.
			}

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


int socket_send(int sn, char *ip, int port, char *buf, size_t buf_size)
{
    char tmpip[20] = {0};
    strcat(tmpip, ip);
	uint8_t tcpc_ip[4]={0};
	int tcpc_port = 1000;
	str_to_netarray(tcpc_ip, 4, tmpip);

    tcpc_port = port;
    int32_t ret; // return value for SOCK_ERRORs
	uint16_t size = 0;
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
            return ssend(sn, buf, buf_size);
            //////////////////////////////////////////////////////////////////////////////////////////////
            break;

        case SOCK_CLOSE_WAIT :
#ifdef _LOOPBACK_DEBUG_
            printf("%d:CloseWait\r\n",sn);
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


int socket_close(int sn){
    return sclose(sn);
}

int socket_disconnect(int sn){
    return sdisconnect(sn);
}

uint8_t g_dns_buf[DATA_BUF_SIZE] = {0};
uint8_t g_tcpip_str[20]= {0};
int dns_host_to_ip(int sn, char *host){
    printf("start dns serve\r\n");
    DNS_init(sn, g_dns_buf);
    printf("started dns serve\r\n");
    uint8_t tcpc_ip[4]={0};
    int ret = 0;
    if ((ret = DNS_run(dns, host, tcpc_ip)) > 0)
    {
        printf("> 1st DNS Respond\r\n");
    }
    else if ((ret != -1) && ((ret = DNS_run(dns_bk, host, tcpc_ip))>0))     // retry to 2nd DNS
    {
        printf("> 2st DNS Respond\r\n");
    }
    sprintf(g_tcpip_str, "%d.%d.%d.%d", tcpc_ip[0],tcpc_ip[1],tcpc_ip[2],tcpc_ip[3]);
    printf("%s---%d.%d.%d.%d\n",g_tcpip_str, tcpc_ip[0],tcpc_ip[1],tcpc_ip[2],tcpc_ip[3]);
    return ret;
}

void dns_get_ip(char *res, size_t *res_size){
     *res_size = strlen(g_tcpip_str);
     printf("size for ip:%d\n", *res_size);
	size_t i=0;
	for(;i<*res_size;i++ ){
        *res++ = g_tcpip_str[i];}
	*res = 0;
}
