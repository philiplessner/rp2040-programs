#ifndef ROTARYENCODER_H_
#define ROTARYENCODER_H_
#include "pico/stdlib.h"

typedef struct {
    uint clk;
    uint dt;
    uint sw;
} RotaryEncoder;

void rotaryInit(RotaryEncoder*);
void rotary(uint, uint32_t);
int8_t checkRotaryEncoder(RotaryEncoder*);
#endif  // ROTARYENCODER_H_
