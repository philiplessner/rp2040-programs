/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include "pico/stdlib.h"
#define LED_PIN 25

int main() {
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    char userInput;
    while (true) {
        printf("Command (1=on or 0=off):\n");
        userInput = getchar();
        
        if(userInput == '1'){
            gpio_put(LED_PIN, 1);
            printf("LED switched on!\n");
        }
        else if(userInput == '0'){
            gpio_put(LED_PIN, 0);
            printf("LED switched oof!\n");
        }
        else {
            printf("Invalid Input!\n");
        }
    }
    return 0;
}
