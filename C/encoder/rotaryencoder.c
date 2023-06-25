#include "pico/stdlib.h"
#include "./rotaryencoder.h"

// Flag from interrupt routine (moved=true)
volatile bool rotaryFlag = false;

void rotaryInit(RotaryEncoder* const me, uint clk, uint dt, uint sw) {
    me->clk = clk;
    me->dt = dt;
    me->sw = sw;
    gpio_init(me->clk);
    gpio_init(me->dt);
    gpio_init(me->sw);
    gpio_set_dir(me->clk, false);
    gpio_set_dir(me->dt, false);
    gpio_set_dir(me->sw, false);
    gpio_pull_up(me->sw);
    gpio_pull_up(me->clk);
    gpio_pull_up(me->dt);
    gpio_set_irq_enabled_with_callback(me->clk,
                                        GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL,
                                        true,
                                        &rotary);
    gpio_set_irq_enabled_with_callback(me->dt,
                                        GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL,
                                        true,
                                        &rotary);
}

// Interrupt routine just sets a flag when rotation is detected
void rotary(uint gpio, uint32_t event_mask) {
    rotaryFlag = true;
}

// Rotary encoder has moved (interrupt tells us) but what happened?
// See https://www.pinteric.com/rotary.html
int8_t checkRotaryEncoder(RotaryEncoder* const me) {
    // Reset the flag that brought us here (from ISR)
    rotaryFlag = false;

    static uint8_t lrmem = 3;
    static int lrsum = 0;
    static int8_t TRANS[] = {0, -1, 1, 14,
                             1, 0, 14, -1,
                             -1, 14, 0, 1,
                             14, 1, -1, 0};

     /* Read BOTH pin states to deterimine 
     validity of rotation (ie not just switch bounce) */
    bool l = gpio_get(me->clk);
    bool r = gpio_get(me->dt);

    // Move previous value 2 bits to the left and add in our new values
    lrmem = ((lrmem & 0x03) << 2) + 2 * l + r;

    /* Convert the bit pattern to a movement indicator 
    (14 = impossible, ie switch bounce) */
    lrsum += TRANS[lrmem];

    /* encoder not in the neutral (detent) state */
    if (lrsum % 4 != 0) {
        return 0;
    }

    /* encoder in the neutral state - clockwise rotation*/
    if (lrsum == 4) {
        lrsum = 0;
        return 1;
    }

    /* encoder in the neutral state - anti-clockwise rotation*/
    if (lrsum == -4) {
        lrsum = 0;
        return -1;
    }

    // An impossible rotation has been detected - ignore the movement
    lrsum = 0;
    return 0;
}
