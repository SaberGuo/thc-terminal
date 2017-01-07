//
// Created by saber on 2016/12/28.
//

#include "commons.h"
#include <stdio.h>
#include <string.h>
const char delims[] = ".-";
uint8_t str_to_netarray(uint8_t *ip, uint8_t num, char *str_ip){
    char *p = strtok(str_ip, delims);
    int i = 0;
    ip[i++] = atoi(p);
    while(p = strtok(NULL, delims)){
        ip[i++] = atoi(p);
    }
    if(i == num){return WIZNET_OK;}

    return WIZNET_ERROR;
}
uint8_t netarray_to_str(char *str_ip, uint8_t *ip, uint8_t num, char *delim){
    char tmp[10]; int i = 0;
    for(;i<num-1;i++){
        sprintf(tmp,"%d%s", ip[i], delim);
        if(!strcat(str_ip, tmp)){
            return WIZNET_ERROR;
        }
    }
    sprintf(tmp, "%d",ip[i]);
    if(!strcat(str_ip, tmp)){
        return WIZNET_ERROR;
    }
    return WIZNET_OK;
}
