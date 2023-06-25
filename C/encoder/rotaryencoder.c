#include "pico/stdlib.h"
#include "./rotaryencoder.h"

// Flag from interrupt routine (moved=true)
volatile bool rotaryEncoder = false;

// Interrupt routine just sets a flag when rotation is detected
void rotary() {
    rotaryEncoder = true;
}

// Rotary encoder has moved (interrupt tells us) but what happened?
// See https://www.pinteric.com/rotary.html
int8_t checkRotaryEncoder(uint clk, uint dt) {
    // Reset the flag that brought us here (from ISR)
    rotaryEncoder = false;

    static uint8_t lrmem = 3;
    static int lrsum = 0;
    static int8_t TRANS[] = {0, -1, 1, 14,
                             1, 0, 14, -1,
                             -1, 14, 0, 1,
                             14, 1, -1, 0};

     /* Read BOTH pin states to deterimine 
     validity of rotation (ie not just switch bounce) */
    bool l = gpio_get(clk);
    bool r = gpio_get(dt);

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
