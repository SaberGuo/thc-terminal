
#include <bcm2835.h>
#include <stdio.h>
#include "loopback.h"
#include "wizchip_conf.h"
#include "ftpd.h"
//#define FTPTEST

void cs_sel(){}
void cs_desel(){}
uint8_t spi_rb(void){
    return bcm2835_spi_transfer(0);
}

void spi_wb(uint8_t b){
    bcm2835_spi_transfer(b);
}

void spi_wb_burst(uint8_t *pbuf, uint16_t len){
    bcm2835_spi_writenb(pbuf, len);
}

void spi_rb_burst(uint8_t *pbuf, uint16_t len){
    bcm2835_spi_transfern(pbuf, len);
}

int main(int argc, char **argv){
   // printf("ok start");


   reg_wizchip_cs_cbfunc(cs_sel, cs_desel);
   reg_wizchip_spi_cbfunc(spi_rb, spi_wb);
   reg_wizchip_spiburst_cbfunc(spi_rb_burst, spi_wb_burst);


   if(!bcm2835_init()){
     // printf("please running as root\n");
      return 1;
   }
   if(!bcm2835_spi_begin()){
     // printf("spi begin error!\n");
     return 1;}
bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64);
bcm2835_spi_chipSelect(BCM2835_SPI_CS0);
bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);
    wiz_NetInfo g_netinfo;
    g_netinfo.mac[0] = 0x0c;
    g_netinfo.mac[1] = 0xeb;
    g_netinfo.mac[2] = 0xa1;
    g_netinfo.mac[3] = 0xa3;
    g_netinfo.mac[4] = 0xc0;
    g_netinfo.mac[5] = 0x01;
    
    g_netinfo.ip[0] = 192;
    g_netinfo.ip[1] = 168;
    g_netinfo.ip[2] = 1;
    g_netinfo.ip[3] = 199;
    
    g_netinfo.sn[0] = 255;
    g_netinfo.sn[1] = 255;
    g_netinfo.sn[2] = 255;
    g_netinfo.sn[3] = 0;

    g_netinfo.gw[0] = 192;
    g_netinfo.gw[1] = 168;
    g_netinfo.gw[2] = 1;
    g_netinfo.gw[3] = 1;

    g_netinfo.dns[0] = 8;
    g_netinfo.dns[1] = 8;
    g_netinfo.dns[2] = 8;
    g_netinfo.dns[3] = 8;

    g_netinfo.dhcp = 1;
    ctlnetwork(CN_SET_NETINFO, (void *)&g_netinfo);
    ctlnetwork(CN_GET_NETINFO, (void *)&g_netinfo);

    printf("mac: 0x%02X 0x%02X 0x%02\n", g_netinfo.mac[0], g_netinfo.mac[1], g_netinfo.mac[2]);
    printf("ip: %d.%d.%d.%d\n", g_netinfo.ip[0], g_netinfo.ip[1], g_netinfo.ip[2], g_netinfo.ip[3]);
    printf("sn: %d.%d.%d.%d\n", g_netinfo.sn[0], g_netinfo.sn[1], g_netinfo.sn[2], g_netinfo.sn[3]);
    printf("gw: %d.%d.%d.%d\n", g_netinfo.gw[0], g_netinfo.gw[1], g_netinfo.gw[2], g_netinfo.gw[3]);
    

    
    uint8_t dstip[4] = {123,57,60,239};
    
#ifdef FTPTEST
    uint8_t gftpbuf[_MAX_SS];
    uint8_t res;
    ftpd_init(g_netinfo.ip);
    while(1){
        res = ftpd_run(gftpbuf);
        if(res ==5) break;
    }
#else
    uint8_t bufs[1024];
    uint8_t bufc[1024];
    while(1){
    loopback_tcpc(0, bufc, dstip, 8000);
    loopback_tcps(1, bufs, 7000); 
    }
#endif
   bcm2835_spi_end();
   bcm2835_close();
}
