#include <stdio.h>
#include "pico/stdlib.h"
#include <stdint.h>
#include "hardware/adc.h"

void adc_setup(uint adc_channel) {
    int adc_gpio[3] = {26, 27, 28};
    adc_init();
    // Make sure GPIO is high-impedance, no pullups etc
    adc_gpio_init(adc_gpio[adc_channel]);
    // Select which channel to read
    adc_select_input(adc_channel);
}

int main() {
    const uint CTRL_PIN = 16;
    const uint extLED_PIN = 12;
    const uint ADC_INPUT = 2;
    const uint ADC_TIME = 1;
    const uint16_t lightLevelThreshold = 600;
    uint16_t ledOnTime = 10000;

    // Send a high signal to the enable pin of the power supply
    gpio_init(CTRL_PIN);
    gpio_set_dir(CTRL_PIN, GPIO_OUT);
    gpio_put(CTRL_PIN, 1);

    stdio_init_all();
    printf("On!\n");
    
    gpio_init(extLED_PIN);
    gpio_set_dir(extLED_PIN, GPIO_OUT);
    adc_setup(ADC_INPUT);
    sleep_ms(500); // Let the ADC stabilize

    // Take Light Sensor Reading
    // 12-bit conversion, assume max value == ADC_VREF == 3.3 V
    uint16_t result = adc_read();
    printf("Light Sensor= %d\n", result);

    // Get setpoint for light on
    adc_setup(ADC_TIME);
    uint16_t rawtime = adc_read();
    printf("Time Adjustment = %d\n", rawtime);
    ledOnTime = (uint16_t)(22.5 * (double)rawtime + 10000.);
    printf("ledOnTime = %d\n",ledOnTime);
    
    if (result < lightLevelThreshold) {
        gpio_put(extLED_PIN, 1);
        sleep_ms(ledOnTime);
    }

    // Finished--Shut send low signal to power supply to shutdown
    gpio_put(CTRL_PIN, 0);
    while(true);
}
