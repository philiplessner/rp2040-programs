# Set minimum required version of CMake
cmake_minimum_required(VERSION 3.13)

# Include build functions from Pico SDK
include(pico_sdk_import.cmake)

# Set name of project (as PROJECT_NAME) and C/C++ standards
project (traffic_light C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Creates a pico-sdk subdirectory in our project for the libraries
pico_sdk_init()


# Tell CMake where to find the executable source file
add_executable(${PROJECT_NAME}
        traffic_light.c
        include/traffic_light.h
        )

# Tell CMake where to find project include files
# PRIVATE==Only for this project
target_include_directories(${PROJECT_NAME} PRIVATE include)

pico_enable_stdio_usb(${PROJECT_NAME} 0)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(${PROJECT_NAME} pico_stdlib)

# create map/bin/hex file etc.
pico_add_extra_outputs(${PROJECT_NAME})
