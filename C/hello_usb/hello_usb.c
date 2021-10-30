/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();
    while (true) {
        printf("Command 1 = on or 0 = off\n");
        /* char userInput = getchar(); */
        /* printf("User typed %c", userInput); */
    }
    return 0;
}
