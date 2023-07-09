#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "debounce.h"
#include "pico/time.h"

// Private functions
static bool debounce_timerISR(struct repeating_timer *t);
static bool RawKeyPressed(uint32_t button);
static void debounce_setFlag(bool flag);

void debounce_init(Debounce* const self, 
                   uint32_t button, 
                   int32_t ms_delay) {
  self->button = button;
  self->ms_delay = ms_delay;
  self->state = 0;
  self->switchFlag = false;
  struct repeating_timer *timer = malloc(sizeof(struct repeating_timer));
  self->timer = timer;
  gpio_set_function(self->button, GPIO_FUNC_SIO);
  gpio_set_dir(self->button, false);
  gpio_pull_up(self->button);
  bool success = add_repeating_timer_ms(self->ms_delay, 
                                        &debounce_timerISR, 
                                        self,
                                        self->timer);                                                 
  if (!success) {
    printf("Addition of Repeating Timer Failed!\n");
  }
}

bool debounce_timerISR(struct repeating_timer *t) {
  Debounce *self = (Debounce *)(t->user_data);
  uint32_t button = self->button;
  uint16_t keyValue = RawKeyPressed(button)?1:0;
  self->state = (self->state << 1) | keyValue | 0xe000;
  if (self->state == 0xf000) {
    self->switchFlag = true;
    self->state = 0;
  }
}

static bool RawKeyPressed(uint32_t button) {
  return gpio_get(button);
}

bool debounce_getFlag(Debounce* const self) {
  return self->switchFlag;
}


void debounce_disableTimerISR(Debounce* const self) {
  bool cancelled = cancel_repeating_timer(self->timer);
}

void debounce_enableTimerISR(Debounce* const self) {
  self->switchFlag = false;
  bool success = add_repeating_timer_ms(self->ms_delay, 
                                   &debounce_timerISR, 
                                   self, 
                                   self->timer);
  if (!success) {
    printf("Addition of Repeating Timer Failed!\n");
  }
}