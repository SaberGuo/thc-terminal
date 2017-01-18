%module wiznet
%include "cstring.i"
%{
#include <stdint.h>
#include <stdio.h>

extern void init_hardware();

extern void init_conf(char *ip, char *mask, char *gateway);

extern int loopback_tcpc(int sn, char *ip, int port);

extern int loopback_tcps(int sn, int port);

extern void tcpc_recv(char *res, size_t *res_size);

extern void tcps_recv(char *res, size_t *res_size);

extern int socket_send(int sn, char *buf, size_t buf_size);

extern int socket_close(int sn);
%}

void init_hardware();

void init_conf(char *ip, char *mask, char *gateway);

int loopback_tcpc(int sn, char *ip, int port);

int loopback_tcps(int sn, int port);

%cstring_output_withsize(char* res,size_t* res_size);
void tcpc_recv(char *res, size_t *res_size);

%cstring_output_withsize(char* res,size_t* res_size);
void tcps_recv(char *res, size_t *res_size);

int socket_send(int sn, char *buf, size_t buf_size);

int socket_close(int sn);

