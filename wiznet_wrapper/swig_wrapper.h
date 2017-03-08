//
// Created by saber on 2016/12/27.
//

#ifndef WIZNET_SWIG_WRAPPER_H
#define WIZNET_SWIG_WRAPPER_H

#include <stdio.h>
#include <stdint.h>
//common methods

/* Loopback test debug message printout enable */
//#define	_LOOPBACK_DEBUG_

/* DATA_BUF_SIZE define for Loopback example */
#ifndef DATA_BUF_SIZE
#define DATA_BUF_SIZE			(2048)
#endif

extern void init_hardware();

extern void init_conf(char *ip, char *mask, char *gateway);

extern int loopback_tcpc(int sn, char *ip, int port);

extern int loopback_tcps(int sn, int port);

extern int dns_host_to_ip(int sn, char *host);

extern void dns_get_ip(char *res, size_t *res_size);

extern void tcpc_recv(char *res, size_t *res_size);

extern void tcps_recv(char *res, size_t *res_size);

extern int socket_send(int sn, char *ip, int port, char *buf, size_t buf_size);

extern int socket_close(int sn);

extern int socket_disconnect(int sn);
#endif //WIZNET_SWIG_WRAPPER_H
