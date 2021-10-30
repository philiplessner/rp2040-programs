// GPIO input button
#include <stdio.h>
#include "pico/stdlib.h"

int main() {
    const uint BUTTON_PIN = 16;
    gpio_init(BUTTON_PIN); 
    gpio_set_dir(BUTTON_PIN, GPIO_IN);
    gpio_pull_down(BUTTON_PIN);
    stdio_init_all();
    while (true) {
        if (gpio_get(BUTTON_PIN)) {
            printf("Button Pressed\n\n");
            sleep_ms(1000);
        }
    }
}
