#ifndef ROTARYENCODER_H_
#define ROTARYENCODER_H_
#include "pico/stdlib.h"

typedef struct {
    uint clk;
    uint dt;
    uint sw;
} RotaryEncoder;

void RotaryEncoder_init(RotaryEncoder* const, uint, uint, uint);
void rotary(uint, uint32_t);
int8_t RotaryEncoder_read(RotaryEncoder* const);
#endif  // ROTARYENCODER_H_
