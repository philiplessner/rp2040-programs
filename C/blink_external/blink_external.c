// Blink an external LED
#include "pico/stdlib.h"

bool repeating_timer_callback(struct repeating_timer *t){
    gpio_xor_mask(3<<8U);
    return true;
}

int main() {
    const uint LEDRed = 8;
    const uint LEDYellow = 9;
    const uint32_t delay = 500;
    gpio_init(LEDRed);
    gpio_init(LEDYellow);
    gpio_set_dir(LEDRed, GPIO_OUT);
    gpio_set_dir(LEDYellow, GPIO_OUT);
    gpio_put(LEDRed, 1);
    gpio_put(LEDYellow, 0);
    struct repeating_timer timer;
    add_repeating_timer_ms(delay, repeating_timer_callback, NULL, &timer);
    while (true) {
        tight_loop_contents();
    }
}
