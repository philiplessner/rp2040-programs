cmake_minimum_required(VERSION 3.10)
include(pico_sdk_import.cmake)
project (button)
pico_sdk_init()
add_executable(button
        button.c
        )

pico_enable_stdio_usb(button 1)
pico_enable_stdio_uart(button 0)
# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(button pico_stdlib)

# create map/bin/hex file etc.
pico_add_extra_outputs(button)

# add url via pico_set_program_url
# example_auto_set_url(blink)
