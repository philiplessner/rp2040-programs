 /* Call an interrupt when a button is presseed */

#include <stdio.h>
#include "pico/sleep.h"
#include "pico/stdlib.h"

const uint buttonPin = 17;
const uint32_t EDGE_FALL = 0x4;
const uint32_t EDGE_RISE = 0x8;
const bool OUTPUT = true;
const bool INPUT = false;
const bool HIGH = true;
const bool LOW = false;

void button_interrupt(uint gpio, uint32_t events) {
  gpio_set_irq_enabled(buttonPin, EDGE_FALL, false);
  printf("Button Pressed\n");
  gpio_set_irq_enabled(buttonPin, EDGE_FALL, true);
}

int main() {
    gpio_init(buttonPin); 
    gpio_set_dir(buttonPin, GPIO_IN);
    gpio_pull_up(buttonPin);
    stdio_init_all();
//  gpio_set_irq_enabled_with_callback(buttonPin, EDGE_FALL, true, &button_interrupt);
    printf("Running from XOSC\n");
    uart_default_tx_wait_blocking();
  sleep_run_from_xosc();
  
  while(true) {
      printf("Going to Sleep\n");
      uart_default_tx_wait_blocking();
      sleep_goto_dormant_until_pin(buttonPin, true, false);
      printf("Button Pressed\n");
      uart_default_tx_wait_blocking();
      sleep_ms(20);
  }
}

