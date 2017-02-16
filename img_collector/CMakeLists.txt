cmake_minimum_required(VERSION 3.0)
#project name
PrOJeCT(W5500_TEST)
#include directory
INCLUDE_DIRECTORIES(include)
AUX_SOURCE_DIRECTORY(src SRC_LIST)
SET(CMAKE_BUILD_TYPE "Debug")
SET(CMAKE_C_FLAGS "-std=c99 -o0 -Wall -Wextra")
SET(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_C_FLAGS} -g -ggdb")
SET(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
#
ADD_EXECUTABLE(img_collector
${SRC_LIST}
)
TARGET_LINK_LIBRARIES(img_collector bcm2835)

