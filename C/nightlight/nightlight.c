#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/timer.h"
#include "pico/sleep.h"

const uint pirPin = 5;
const uint ledPin = 15;
const uint lightSensorPin = 26;
const uint32_t EDGE_RISE = 0x8;
const bool OUTPUT = true;
const bool INPUT = false;
const bool HIGH = true;
const bool LOW = false;

void pir_interrupt(uint gpio, uint32_t events) {
  const uint16_t lightLevelThreshold = 300;
  const uint32_t interval = 2000;
  gpio_set_irq_enabled(pirPin, EDGE_RISE, false);
  uint16_t lightLevel = adc_read();
  if (lightLevel < lightLevelThreshold) {
      gpio_put(ledPin, HIGH);
      absolute_time_t currentTime = get_absolute_time();
      absolute_time_t timeOff = make_timeout_time_ms(interval);
      int64_t timeDiff = absolute_time_diff_us(currentTime, timeOff);
      while (timeDiff > 0) {
        currentTime = get_absolute_time();
        timeDiff = absolute_time_diff_us(currentTime, timeOff);
      }
      gpio_put(ledPin, LOW);
      }
  gpio_set_irq_enabled(pirPin, EDGE_RISE, true);
}

int main() {
  const uint32_t sleepTime = 1;
  gpio_init(pirPin);
  gpio_set_dir(pirPin, INPUT);
  gpio_init(ledPin);
  gpio_set_dir(ledPin, OUTPUT);
  adc_init();
  adc_gpio_init(lightSensorPin);
  adc_select_input(0);
  gpio_set_irq_enabled_with_callback(pirPin, EDGE_RISE, true, &pir_interrupt);
  gpio_put(ledPin, LOW);
  
  while(true) {
//    sleep_ms(sleepTime);
    sleep_goto_dormant_until_edge_high(pirPin);
  }
}


