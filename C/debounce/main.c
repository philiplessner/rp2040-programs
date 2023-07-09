#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/time.h"
#include "./debounce.h"

#define ENCODER_SW 18
#define MY_BUTTON  19
#define RED_LED    12
#define GREEN_LED  10
#define CHECK_MS    1

int main() {
  stdio_init_all();
  Debounce encoderSW;
  Debounce mybutton;
  debounce_init(&mybutton, MY_BUTTON, CHECK_MS);
  debounce_init(&encoderSW, ENCODER_SW, CHECK_MS);
  // Initialize LEDs
  gpio_set_function(RED_LED, GPIO_FUNC_SIO);
  gpio_set_dir(RED_LED, true);
  gpio_set_function(GREEN_LED, GPIO_FUNC_SIO);
  gpio_set_dir(GREEN_LED, true);

  while (true) {
    if (debounce_getFlag(&encoderSW)) {
      debounce_disableTimerISR(&encoderSW);
      gpio_put(RED_LED, true);
      sleep_ms(250);
      gpio_put(RED_LED, false);
      debounce_enableTimerISR(&encoderSW);
    }
    if (debounce_getFlag(&mybutton)) {
      debounce_disableTimerISR(&mybutton);
      gpio_put(GREEN_LED, true);
      sleep_ms(250);
      gpio_put(GREEN_LED, false);
      debounce_enableTimerISR(&mybutton);
    }
  }
}
