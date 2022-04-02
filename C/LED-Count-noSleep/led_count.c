/*
Binary count 0 to 15 in continous loop
Pressing button resets to 0
*/

#include "pico/stdlib.h"
#include "binarycount.h"

volatile bool interrupt_flag = false;

int main() {
  
  absolute_time_t currentTime;
  count_t myCount = {0,
                   0,
                   0,
                   1000};

  
  for (uint32_t i = LED_PIN_MIN; i < LED_PIN_MAX+1; i++) {
    myCount.mask |=  1 << i;
  }
  gpio_init_mask(myCount.mask);
  gpio_set_dir_out_masked(myCount.mask);
  gpio_init(RESET_BUTTON);
  gpio_set_input_enabled(RESET_BUTTON, true);
  gpio_pull_up(RESET_BUTTON);
  gpio_set_irq_enabled_with_callback(RESET_BUTTON, GPIO_IRQ_EDGE_FALL, true, (gpio_irq_callback_t) &button_interrupt_callback);
  
  reset(&myCount);
  
  while (true) {
    currentTime = get_absolute_time();

    if (interrupt_flag) {
      currentTime = get_absolute_time();
      reset(&myCount);
      interrupt_flag = false;
      gpio_set_irq_enabled_with_callback(RESET_BUTTON, GPIO_IRQ_EDGE_FALL, true, (gpio_irq_callback_t) &button_interrupt_callback);
    }

    if (currentTime >= myCount.tToggle) {
      if (myCount.count < 16) {
        increment(&myCount);
      }
      else {
        reset(&myCount);
      }
    }
    
    
  }
}


void increment(count_t *myCount) {
  myCount->count += 1;
  myCount->tToggle = make_timeout_time_ms(myCount->delayTime);
  gpio_put_masked(myCount->mask, myCount->count << LED_PIN_MIN);
  return;
}

void reset(count_t *myCount) {
  myCount->count = 0;
  myCount->tToggle = make_timeout_time_ms(myCount->delayTime);
  gpio_put_all(0);
  return;
}

gpio_irq_callback_t button_interrupt_callback(uint gpio, uint32_t events) {
  gpio_set_irq_enabled(gpio, events, false);
  interrupt_flag = true;
}
