#include <string.h>
#include "pico/stdlib.h"
#include "./rotaryencoder.h"

// Private variables and function
// Flag from interrupt routine (moved=true)
static volatile bool rotaryFlag = false;
static void RotaryEncoder_ISR(uint, uint32_t);

void RotaryEncoder_init(RotaryEncoder* const self, uint clk, uint dt, uint sw) {
    memset(self, 0, sizeof(*self));
    self->clk = clk;
    self->dt = dt;
    self->sw = sw;
    gpio_init(self->clk);
    gpio_init(self->dt);
    gpio_init(self->sw);
    gpio_set_dir(self->clk, false);
    gpio_set_dir(self->dt, false);
    gpio_set_dir(self->sw, false);
    gpio_pull_up(self->sw);
    gpio_pull_up(self->clk);
    gpio_pull_up(self->dt);
    gpio_set_irq_enabled_with_callback(self->clk,
                                        GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL,
                                        true,
                                        &RotaryEncoder_ISR);
    gpio_set_irq_enabled_with_callback(self->dt,
                                        GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL,
                                        true,
                                        &RotaryEncoder_ISR);
}

// Interrupt routine just sets a flag when rotation is detected
static void RotaryEncoder_ISR(uint gpio, uint32_t event_mask) {
    rotaryFlag = true;
}

bool RotaryEncoder_getISRFlag() {
    return rotaryFlag;
}

// Rotary encoder has moved (interrupt tells us) but what happened?
// See https://www.pinteric.com/rotary.html
int8_t RotaryEncoder_read(RotaryEncoder* const self) {
    // Reset the flag that brought us here (from ISR)
    rotaryFlag = false;

    static uint8_t lrselfm = 3;
    static int lrsum = 0;
    static int8_t TRANS[] = {0, -1, 1, 14,
                             1, 0, 14, -1,
                             -1, 14, 0, 1,
                             14, 1, -1, 0};

     /* Read BOTH pin states to deterimine 
     validity of rotation (ie not just switch bounce) */
    bool l = gpio_get(self->clk);
    bool r = gpio_get(self->dt);

    // Move previous value 2 bits to the left and add in our new values
    lrselfm = ((lrselfm & 0x03) << 2) + 2 * l + r;

    /* Convert the bit pattern to a moveselfnt indicator 
    (14 = impossible, ie switch bounce) */
    lrsum += TRANS[lrselfm];

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

    // An impossible rotation has been detected - ignore the moveselfnt
    lrsum = 0;
    return 0;
}
