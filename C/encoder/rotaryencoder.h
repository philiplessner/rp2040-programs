#ifndef ROTARYENCODER_H_
#define ROTARYENCODER_H_
#include "pico/stdlib.h"

typedef struct {
    uint clk;
    uint dt;
    uint sw;
} RotaryEncoder;

// Public interface functions
void RotaryEncoder_init(RotaryEncoder* const, uint, uint, uint);
int8_t RotaryEncoder_read(RotaryEncoder* const);
bool RotaryEncoder_getISRFlag();
#endif  // ROTARYENCODER_H_
