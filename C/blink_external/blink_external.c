/* Blink 3 external LEDs using timer interrupt
 The other LED is blinked in the main loop
 */

#include "pico/stdlib.h"
#include <stdio.h>
#define LEDRed 8
#define LEDYellow 9
#define LEDGreen 10
#define LEDBlue 11

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
    const uint32_t timeOn = 3000; // Time after the Blue LED is toggled in ms
    absolute_time_t timeOff;

    gpio_init_mask(mask);
    gpio_set_dir_out_masked(mask);
    gpio_put_masked(mask, 0);
    gpio_init(LEDBlue);
    gpio_set_dir(LEDBlue, 1);
    struct repeating_timer timer;
    add_repeating_timer_ms(delay, repeating_timer_callback, NULL, &timer);
    timeOff = make_timeout_time_ms(timeOn); // Absolute time after the Blue LED is toggled

    while (true) {
        if(time_reached(timeOff)) {
            gpio_xor_mask(1U<<LEDBlue);
            timeOff = make_timeout_time_ms(timeOn); // Reset the time
        }
    }
}
