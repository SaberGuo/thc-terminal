#! /bin/bash

swig -python wiznet.i
gcc -c -fPIC wiznet_wrap.c swig_wrapper.c commons.c rpi.c socket.c wizchip_conf.c w5500.c -I. -I/usr/include/python2.7
gcc -shared wiznet_wrap.o swig_wrapper.o rpi.o socket.o commons.o wizchip_conf.o w5500.o -o _wiznet.so -lbcm2835
