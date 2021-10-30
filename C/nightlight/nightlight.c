#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/timer.h"

const uint pirPin = 5;
const uint ledPin = 15;
const uint lightSensorPin = 26;
const uint32_t interval = 2000;
const uint16_t lightLevelThreshold = 300;
const uint32_t sleepTime = 1;
const uint32_t EDGE_RISE = 0x8;
absolute_time_t currentTime;
absolute_time_t timeOff;
int64_t timeDiff;
uint16_t lightLevel;

void pir_interrupt(uint gpio, uint32_t events) {
  gpio_set_irq_enabled(pirPin, EDGE_RISE, false);
  lightLevel = adc_read();
  if (lightLevel < lightLevelThreshold) {
      gpio_put(ledPin, true);
      currentTime = get_absolute_time();
      timeOff = make_timeout_time_ms(interval);
      timeDiff = absolute_time_diff_us(currentTime, timeOff);
      while (timeDiff > 0) {
        currentTime = get_absolute_time();
        timeDiff = absolute_time_diff_us(currentTime, timeOff);
      }
      gpio_put(ledPin, false);
      }
  gpio_set_irq_enabled(pirPin, EDGE_RISE, true);
}

int main() {

  gpio_init(pirPin);
  gpio_set_dir(pirPin, false);
  gpio_init(ledPin);
  gpio_set_dir(ledPin, true);
  adc_init();
  adc_gpio_init(lightSensorPin);
  adc_select_input(0);
  gpio_set_irq_enabled_with_callback(pirPin, EDGE_RISE, true, &pir_interrupt);
  gpio_put(ledPin, false);
  
  while(true) {
    sleep_ms(sleepTime);
  }
}


