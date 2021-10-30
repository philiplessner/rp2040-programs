cmake_minimum_required(VERSION 3.10)
include(pico_sdk_import.cmake)
project(adc_pot)
pico_sdk_init()
add_executable(adc_pot
        adc_pot.c
        )

pico_enable_stdio_usb(adc_pot 1)
pico_enable_stdio_uart(adc_pot 0)
target_link_libraries(adc_pot pico_stdlib hardware_adc)

# create map/bin/hex file etc.
pico_add_extra_outputs(adc_pot)

