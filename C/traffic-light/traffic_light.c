#include <stdio.h>
#include "pico/stdlib.h"
#include "traffic_light.h"

int main() {
  uint32_t mask;
  int state;
  absolute_time_t currentTime;
  absolute_time_t yellowTime;

  for(int i=RED; i<=GREEN; i++) {
    mask |= 1<<i;
  }
  gpio_init_mask(mask);
  gpio_set_dir_out_masked(mask);
  gpio_init(GREEN_BUTTON);
  gpio_set_input_enabled(GREEN_BUTTON, true);
  gpio_pull_up(GREEN_BUTTON);
  gpio_init(RED_BUTTON);
  gpio_set_input_enabled(RED_BUTTON, true);
  gpio_pull_up(RED_BUTTON);
  state = RED;
  gpio_put(RED, true);
  
  while (true) {
    currentTime = get_absolute_time();
  
    switch (state) {
    case(GREEN):
      if(button_pressed(RED_BUTTON)) {
        gpio_put(GREEN, false);
        gpio_put(YELLOW, true);
        state = YELLOW;
        yellowTime = make_timeout_time_ms(yellowDelay);
      }
    break;
    case(YELLOW):
      if (currentTime >= yellowTime) {
        gpio_put(YELLOW, false);
        gpio_put(RED, true);
        state = RED;
      }
    break;
    case(RED):
      if(button_pressed(GREEN_BUTTON)) {
        gpio_put(RED, false);
        gpio_put(GREEN, true);
        state = GREEN;
      }
    break;
  }
  }
}

bool button_pressed(const int button) {
  return !gpio_get(button);
}