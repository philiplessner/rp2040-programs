// Blink 3 external LEDs using timer interrupt

#include "pico/stdlib.h"
#define LEDRed 8
#define LEDYellow 9
#define LEDGreen 10

static const uint32_t mask = 1U << LEDRed | 1U << LEDYellow | 1U << LEDGreen;

bool repeating_timer_callback(struct repeating_timer *t){
    static uint32_t count;
    uint32_t vmask;

    count++;

    switch (count){
        case 1:
            vmask = 1U << LEDRed;
            gpio_put_masked(mask, vmask);
            break;
        case 2:
            vmask = 1U << LEDYellow;
            gpio_put_masked(mask, vmask);
            break;
        case 3:
            vmask = 1U << LEDGreen;
            gpio_put_masked(mask, vmask);
            count = 0;
            break;
    }
    return true;
}

int main() {
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
