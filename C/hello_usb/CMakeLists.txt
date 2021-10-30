cmake_minimum_required(VERSION 3.10)
include(pico_sdk_import.cmake)
project (hello_usb)
pico_sdk_init()
add_executable(hello_usb
        hello_usb.c
        )

pico_enable_stdio_usb(hello_usb 1)
pico_enable_stdio_uart(hello_usb 0)
# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(hello_usb pico_stdlib)

# create map/bin/hex file etc.
pico_add_extra_outputs(hello_usb)

# add url via pico_set_program_url
# example_auto_set_url(blink)
