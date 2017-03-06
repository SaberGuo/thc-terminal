//
// Created by saber on 2016/12/14.
//

#include <bcm2835.h>
#include <stdio.h>

void bcm2835_initlize(){
    if(!bcm2835_init()){
        printf("bcm2835 init fail! please run as root!\n");
    }
    if(!bcm2835_spi_begin()){
        printf("bcm2835 spi init fail! please run as root!\n");
    }
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);      // The default
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);                   // The default
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_8); // 6.250MHz on RPI3
    bcm2835_spi_chipSelect(BCM2835_SPI_CS1);                      // chip select 0
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);      // low for enable chip
}

void   wizchip_cs_sel(){}
void   wizchip_cs_desel(){}
/**
 * @brief Default function to read in SPI interface.
 * @note This function help not to access wrong address. If you do not describe this function or register any functions,
 * null function is called.
 */
//uint8_t wizchip_spi_readbyte(void)        {return 0;};
uint8_t rpi_spi_readbyte(void){
    return bcm2835_spi_transfer(0);
}

/**
 * @brief Default function to write in SPI interface.
 * @note This function help not to access wrong address. If you do not describe this function or register any functions,
 * null function is called.
 */
//void 	wizchip_spi_writebyte(uint8_t wb) {};
void 	rpi_spi_writebyte(uint8_t wb){
    bcm2835_spi_transfer(wb);
}

/**
 * @brief Default function to burst read in SPI interface.
 * @note This function help not to access wrong address. If you do not describe this function or register any functions,
 * null function is called.
 */
//void 	wizchip_spi_readburst(uint8_t* pBuf, uint16_t len) 	{};
void 	rpi_spi_readburst(uint8_t* pBuf, uint16_t len){
    bcm2835_spi_transfern((char*)pBuf, len);
}

/**
 * @brief Default function to burst write in SPI interface.
 * @note This function help not to access wrong address. If you do not describe this function or register any functions,
 * null function is called.
 */
//void 	wizchip_spi_writeburst(uint8_t* pBuf, uint16_t len) {};
void 	rpi_spi_writeburst(uint8_t* pBuf, uint16_t len){
    bcm2835_spi_writenb((char*)pBuf, len);
}
