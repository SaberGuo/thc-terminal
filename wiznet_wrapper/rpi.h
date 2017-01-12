//
// Created by saber on 2016/12/14.
//

#ifndef WIZNET_RPI_H
#define WIZNET_RPI_H
#include <stdint.h>

extern void bcm2835_initlize();

extern void   wizchip_cs_sel();
extern void   wizchip_cs_desel();
extern uint8_t rpi_spi_readbyte(void);
extern void 	rpi_spi_writebyte(uint8_t wb);
extern void 	rpi_spi_readburst(uint8_t* pBuf, uint16_t len);
extern void 	rpi_spi_writeburst(uint8_t* pBuf, uint16_t len);

#endif //WIZNET_RPI_H
