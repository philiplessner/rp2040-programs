/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"

int main() {
    const uint relayPin = 12;
    gpio_init(relayPin);
    gpio_set_dir(relayPin, GPIO_OUT);
    while (true) {
        gpio_put(relayPin, 1);
        sleep_ms(5000);
        gpio_put(relayPin, 0);
        sleep_ms(5000);
    }
}
