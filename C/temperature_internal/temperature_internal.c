#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
 
int main() {
    stdio_init_all();
    printf("ADC Example, measuring on-board temperature\n");
 
    adc_init();
    // Enable temperature sensor
    adc_set_temp_sensor_enabled(true);
    // Make sure GPIO is high-impedance, no pullups etc
    /* adc_gpio_init(26); */
    // Select ADC input 4 (internal temperature sensor)
    adc_select_input(4);
 
    while (1) {
        // 12-bit conversion, assume max value == ADC_VREF == 3.3 V
        const float conversion_factor = 3.3f / (1 << 12);
        uint16_t result = adc_read();
        float ADC_Voltage = result * conversion_factor;
        float temperature = 27.0 - (ADC_Voltage - 0.706)/0.001721;
        printf("Raw value: 0x%03x, voltage: %f V, T %f C\n", result, ADC_Voltage, temperature);
        sleep_ms(1000);
    }
}
