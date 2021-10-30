cmake_minimum_required(VERSION 3.10)
include(pico_sdk_import.cmake)
project(dht)
pico_sdk_init()
add_executable(dht
        dht.c
        )

pico_enable_stdio_usb(dht 1)
pico_enable_stdio_uart(dht 0)

target_link_libraries(dht pico_stdlib)

pico_add_extra_outputs(dht)

# add url via pico_set_program_url
#example_auto_set_url(dht)

