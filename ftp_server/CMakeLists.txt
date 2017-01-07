cmake_minimum_required(VERSION 3.0)
#project name
PrOJeCT(W5500_TEST)
#include directory
INCLUDE_DIRECTORIES(W5500 .)
#AUX_SOURCE_DIRECTORY(src SRC_LIST)
SET(CMAKE_BUILD_TYPE "Debug")
SET(CMAKE_C_FLAGS "-std=c99 -o0 -Wall -Wextra")
SET(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_C_FLAGS} -g -ggdb")
SET(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
#
ADD_EXECUTABLE(w5500_tcp 
main.c
#spi_w5500.c
wizchip_conf.c
socket.c
ftpd.c
ff.c
loopback.c
W5500/w5500.c
)
TARGET_LINK_LIBRARIES(w5500_tcp bcm2835)

