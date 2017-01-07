// spi.c
//
// Example program for bcm2835 library
// Shows how to interface with SPI to transfer a byte to and from an SPI device
//
// After installing bcm2835, you can build this 
// with something like:
// gcc -o spi spi.c -l bcm2835
// sudo ./spi
//
// Or you can test it before installing with:
// gcc -o spi -I ../../src ../../src/bcm2835.c spi.c
// sudo ./spi
//
// Author: Mike McCauley
// Copyright (C) 2012 Mike McCauley
// $Id: RF22.h,v 1.21 2012/05/30 01:51:25 mikem Exp $

#include <bcm2835.h>
#include <stdio.h>
#define OPT 0x03
#define CS1 RPI_GPIO_P1_26
void write_w5500_bytes(uint8_t* add,uint8_t len_addr, uint8_t* value, uint8_t len_value){
    bcm2835_spi_writenb(add,len_addr);
    uint8_t act = 0;
    uint8_t i = 0;
    if(len_value ==1){ act = 1;}
    if(len_value == 2){ act = 2;}
    if(len_value == 4){act = 3;}
    uint8_t write_act = 0x04+act;
    bcm2835_spi_writenb(&write_act, 1);
    bcm2835_spi_transfern(value, len_value);
    //for(i=0;i<len_value;i++){
    //    bcm2835_spi_transfern(value++, 1);
    //}
}
void write_socket_bytes(uint8_t socket, uint8_t* add, uint8_t* value, uint8_t len_value){
    bcm2835_spi_writenb(add, 2);
    uint8_t act = 0;
    if(len_value ==1){ act = 1;}
    if(len_value == 2){ act = 2;}
    if(len_value == 4){act = 3;}
    uint8_t write_act = 0x20*socket+0x08+0x04+act;
    bcm2835_spi_writenb(&write_act, 1);
    bcm2835_spi_transfern(value, len_value);
}
void read_socket_bytes(uint8_t socket, uint8_t* add, uint8_t* value, uint8_t len_value){
    bcm2835_spi_writenb(add, 2);
    uint8_t act = 0;
    if(len_value ==1){ act = 1;}
    if(len_value == 2){ act = 2;}
    if(len_value == 4){act = 3;}
    uint8_t write_act = 0x20*socket+0x08+act;
    bcm2835_spi_writenb(&write_act, 1);
    bcm2835_spi_transfern(value, len_value);
}

void read_w5500_bytes(uint8_t* add, uint8_t len_addr, uint8_t* res, uint8_t len_res){
    bcm2835_spi_writenb(add,len_addr);
    uint8_t act = 0;
    if(len_res ==1){ act = 1;}
    if(len_res == 2){ act = 2;}
    if(len_res == 4){act = 3;}
    uint8_t write_act = act;
    bcm2835_spi_writenb(&write_act, 1);
    bcm2835_spi_transfern(res, len_res);
    
}
void print_res(char* dsc, uint8_t* res, uint8_t len_res){
    uint8_t i = 0;
    printf(dsc);
    for(i=0;i<len_res;++i){
        printf("%d,",res[i]);
    }
    printf("\n");
}
void socket_connect(uint8_t socket){
    uint8_t sn_mr[2] = {0,0};
    uint8_t mr_tcp[1] = {0x01};
    uint8_t mr_tcp_res[1];
    write_socket_bytes(0,sn_mr, mr_tcp,1);
    read_socket_bytes(0,sn_mr, mr_tcp_res,1);
    print_res("mode:", mr_tcp_res, 1);

    uint8_t sn_cr[2] = {0,1};
    uint8_t cr_open[1] = {0x01};
    uint8_t cr_open_res[1];
    write_socket_bytes(0, sn_cr, cr_open, 1);
    read_socket_bytes(0,sn_cr, cr_open_res,1);
    print_res("status:", cr_open_res, 1);
    delay(5);
    uint8_t sn_sr[2] = {0,3};
    uint8_t sr_res[1] = {0x00};
    read_socket_bytes(0, sn_sr, sr_res, 1);
    print_res("socket status:", sr_res, 1);


    cr_open[0] = 0x04;
    write_socket_bytes(0, sn_cr, cr_open, 1);
    read_socket_bytes(0,sn_cr, cr_open_res,1);
    print_res("status:", cr_open_res, 1);
    

    
    

}

void write_socket_data_buffer(uint8_t socket, uint8_t *dat_ptr, uint8_t size){

    uint8_t offset[2], offset1[2];
    uint16_t offset_short, offset1_short;
    uint16_t i;
    uint8_t sn_tx_wr[2]={0, 0x24};
    read_socket_bytes(socket, sn_tx_wr, offset, 2);
    offset_short = offset[0]*256+offset[1];
    offset1_short = offset_short;
    offset_short&=(2048-1);

    offset[0] = (offset_short>>8)&0xff;
    offset[1] = offset_short&0x00ff;
    bcm2835_spi_writenb(offset, 2);
    

}
int main(int argc, char **argv)
{
    // If you call this, it will not actually access the GPIO
// Use for testing
//        bcm2835_set_debug(1);

    if (!bcm2835_init())
    {
      printf("bcm2835_init failed. Are you running as root??\n");
      return 1;
    }

    if (!bcm2835_spi_begin())
    {
      printf("bcm2835_spi_begin failedg. Are you running as root??\n");
      return 1;
    }
    bcm2835_gpio_fsel(CS1, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_write(CS1, LOW);
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);      // The default
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);                   // The default
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_65536); // The default
    bcm2835_spi_chipSelect(BCM2835_SPI_CS0);                      // The default
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);      // the default
    
    // Send a byte to the slave and simultaneously read a byte back from the slave
    // If you tie MISO to MOSI, you should read back what was sent


    uint8_t phycfgr[2] = {0, 0x2e};
    uint8_t ph_res[1];
    read_w5500_bytes(phycfgr, 2, ph_res, 1);
    print_res("phy status:", ph_res, 1);
    
    uint8_t mr[2] = {0,0};
    uint8_t mr_res[1];
    write_w5500_bytes(mr, 2, mr_res, 1);
    
    uint8_t gar[2] = {0,1};
    uint8_t gatway_ip[4] = {192,168,1,1};
    uint8_t gatway_ip_res[4] = {0,0,0,0};
    write_w5500_bytes(gar,2,gatway_ip,4);
    uint8_t subr[2] = {0, 5};
    uint8_t sub_mask[4] = {255,255,255,0};
    uint8_t sub_mask_res[4] = {0,0,0,0};
    write_w5500_bytes(subr, 2, sub_mask, 4);
    uint8_t shar[2] = {0, 9};
    uint8_t phy[6] = {0x0c,0x29, 0xab, 0x7c, 0x00, 0x01};
    uint8_t phy_res[6] = {0,0,0,0};
    write_w5500_bytes(shar, 2, phy, 4);
    shar[1]+=4;
    write_w5500_bytes(shar, 2, phy+4,2);
    shar[1] = 9;
    read_w5500_bytes(shar, 2, phy_res, 4);
    shar[1]+=4;
    read_w5500_bytes(shar, 2, phy_res+4,2);
    print_res("phy res:",phy_res, 6);


    uint8_t sipr[2] = {0, 0x0f};
    uint8_t ip_addr[4] = {192,168,1,199};
    uint8_t ip_addr_res[4] = {0};
    write_w5500_bytes(sipr, 2, ip_addr, 4);
    
    uint8_t rxbuf_size[2] = {0x00, 0x1e};
    uint8_t size_res[1]={2};
    write_socket_bytes(0, rxbuf_size, size_res,1);
    uint8_t txbuf_size[2] = {0, 0x1f};
    write_socket_bytes(0, txbuf_size, size_res,1);

    
    uint8_t rtr[2] = {0x00, 0x19};
    uint8_t rcr[2] = {0, 0x1b};

    uint8_t rtr_res[2]={0x07, 0xd0};
    uint8_t rcr_res[1] = {0x08};

    write_w5500_bytes(rtr, 2, rtr_res, 2);
    write_w5500_bytes(rcr, 2, rcr_res, 1);
    
    uint8_t sn_mssr[2] = {0x00, 0x12};
    uint8_t mssr_res[2] = {0x05, 0xb4};
    write_socket_bytes(0, sn_mssr, mssr_res, 2);



    
    uint8_t sn_port[2] = {0, 4};
    uint8_t s0_port[2] = {0x13, 0x88};
    uint8_t s0_port_res[2] = {0};
    write_socket_bytes(0, sn_port, s0_port, 2);
   // read_socket_bytes(0, sn_port, s0_port_res, 2);
   // print_res("self port:",s0_port_res, 2);

    
    uint8_t sn_dipr[2] = {0,0x10};
    uint8_t s0_dport[2] = {0x17, 0x70};
    uint8_t s0_dport_res[2] = {0};
    write_socket_bytes(0, sn_dipr, s0_dport, 2);
    //read_socket_bytes(0, sn_dipr, s0_dport_res, 2);
    //print_res("dst port:", s0_dport_res, 2);

    
    uint8_t sn_dportr[2] = {0, 0x0c};
    uint8_t dip[4] = {192,168,1,100};
    uint8_t dip_res[4] = {0,0,0,0};
    write_socket_bytes(0,sn_dportr,dip,4);
    //read_socket_bytes(0,sn_dportr,dip_res,4);
    //print_res("dst ip res:",dip_res, 4);
    read_w5500_bytes(gar,2,gatway_ip_res,4);
    print_res("gateway res:",gatway_ip_res, 4);
    read_w5500_bytes(subr,2, sub_mask_res,4);
    print_res("sub mask res:",sub_mask_res, 4);
    read_w5500_bytes(sipr,2, ip_addr_res, 4);
    print_res("self ip:", ip_addr_res, 4);

    socket_connect(0);
    
    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}

