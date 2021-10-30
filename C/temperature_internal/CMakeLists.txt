cmake_minimum_required(VERSION 3.10)
include(pico_sdk_import.cmake)
project (temperature_internal)
pico_sdk_init()
add_executable(temperature_internal
        temperature_internal.c
        )

pico_enable_stdio_usb(temperature_internal 0)
pico_enable_stdio_uart(temperature_internal 1)
# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(temperature_internal pico_stdlib hardware_adc)

# create map/bin/hex file etc.
pico_add_extra_outputs(temperature_internal)

# add url via pico_set_program_url
# example_auto_set_url(blink)
