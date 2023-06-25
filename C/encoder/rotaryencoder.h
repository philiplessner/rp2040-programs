#ifndef ROTARYENCODER_H_
#define ROTARYENCODER_H_
#include "pico/stdlib.h"

typedef struct {
    uint clk;
    uint dt;
    uint sw;
} RotaryEncoder;

void rotaryInit(RotaryEncoder* const, uint, uint, uint);
void rotary(uint, uint32_t);
int8_t checkRotaryEncoder(RotaryEncoder* const);
#endif  // ROTARYENCODER_H_
