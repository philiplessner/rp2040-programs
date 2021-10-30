cmake_minimum_required(VERSION 3.10)
include(pico_sdk_import.cmake)
project (button2)
pico_sdk_init()
add_executable(button2
        button2.c
        )

pico_enable_stdio_usb(button2 1)
pico_enable_stdio_uart(button2 0)
# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(button2 pico_stdlib)

# create map/bin/hex file etc.
pico_add_extra_outputs(button2)

# add url via pico_set_program_url
# example_auto_set_url(blink)
