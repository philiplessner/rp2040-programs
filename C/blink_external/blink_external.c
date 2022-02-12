// Blink an external LED
#include "pico/stdlib.h"

const uint LEDRed = 8;
const uint LEDYellow = 9;
const uint LEDGreen = 10;

bool repeating_timer_callback(struct repeating_timer *t){
    static uint32_t count;

    count++;

    switch (count){
        case 1:
            gpio_put(LEDRed, 1);
            gpio_put(LEDYellow, 0);
            gpio_put(LEDGreen, 0);
            break;
        case 2:
            gpio_put(LEDRed, 0);
            gpio_put(LEDYellow, 1);
            gpio_put(LEDGreen, 0);
            break;
        case 3:
            gpio_put(LEDRed, 0);
            gpio_put(LEDYellow, 0);
            gpio_put(LEDGreen, 1);
            break;
        default:
            count = 0;
    }
    return true;
}

int main() {
    const uint32_t mask = 1U<<LEDRed | 1U<<LEDYellow | 1U<<LEDGreen;
    const uint32_t delay = 500;
    gpio_init_mask(mask);
    gpio_set_dir_out_masked(mask);
    gpio_put_masked(mask, 0);
    struct repeating_timer timer;
    add_repeating_timer_ms(delay, repeating_timer_callback, NULL, &timer);
    while (true) {
        tight_loop_contents();
    }
}
