//
// Created by saber on 2016/12/28.
//

#ifndef WIZNET_COMMONS_H
#define WIZNET_COMMONS_H

#define WIZNET_OK    1
#define WIZNET_ERROR 0

#define _WIZNET_DEBUG_ 1
#include <stdint.h>

extern uint8_t str_to_netarray(uint8_t *ip, uint8_t num, char *str_ip);
extern uint8_t netarray_to_str(char *str_ip, uint8_t *ip, uint8_t num,char *delim);
#endif //WIZNET_COMMONS_H
