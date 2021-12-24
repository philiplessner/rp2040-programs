// GPIO input button
#include <stdio.h>
#include "pico/stdlib.h"

int main() {
    const uint BUTTON_PIN = 17;
    bool prevState = true;
    bool currentState;
    gpio_init(BUTTON_PIN); 
    gpio_set_dir(BUTTON_PIN, GPIO_IN);
    gpio_pull_up(BUTTON_PIN);
    stdio_init_all();
    while (true) {
        currentState = gpio_get(BUTTON_PIN);
        if (prevState && !currentState) {
            printf("Button Pressed\n");
        }
        prevState = currentState;
        sleep_ms(20);
        /*
        if (!gpio_get(BUTTON_PIN)) {
            printf("Button Pressed\n");
            sleep_ms(150);
        } */
    }
}
