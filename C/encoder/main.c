#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/i2c.h"
#include "lcd.h"

#define ENCODER_CLK 16
#define ENCODER_DT  17
#define ENCODER_SW  18
#define INPUT       0
#define LOW         0
#define HIGH        1
#define POT_PIN     28
#define NMENU       3
#define CW          1
#define CCW         2

const uint32_t TIME_READ = 1000;
const uint32_t BAUD_RATE = 100000;
extern volatile bool rotaryEncoder;
typedef struct {
    int32_t state;
    int8_t  rotationValue;
    uint16_t potValue;
  } State;
const char msg[4][20] = {
                           "LED Intensity",
                           "LED On Time",
                           "Light Threshold",
                           "Exit Setup"
                          };

void handleEncoder(State*);
void rotary();
int8_t checkRotaryEncoder();
void handleLEDOnTime();
void handleLEDIntensity();
void handleLightThreshold();
void handleExitSetup();

int main() {
  State rotaryState = {0, 0, 0};

  stdio_init_all();
  // Encoder Setup
  gpio_init(ENCODER_CLK);
  gpio_init(ENCODER_DT);
  gpio_init(ENCODER_SW);
  gpio_set_dir(ENCODER_CLK, INPUT);
  gpio_set_dir(ENCODER_DT, INPUT);
  gpio_set_dir(ENCODER_SW, INPUT);
  gpio_pull_up(ENCODER_SW);
  gpio_pull_up(ENCODER_CLK);
  gpio_pull_up(ENCODER_DT);
  gpio_set_irq_enabled_with_callback(ENCODER_CLK, GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL, true, &rotary);
  gpio_set_irq_enabled_with_callback(ENCODER_DT, GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL, true, &rotary);
  // Potentiometer Setup
  adc_init();
  adc_gpio_init(POT_PIN);
  adc_select_input(2);
  // LCD Setup
  i2c_init(i2c_default, BAUD_RATE);
  gpio_set_function(PICO_DEFAULT_I2C_SDA_PIN, GPIO_FUNC_I2C);
  gpio_set_function(PICO_DEFAULT_I2C_SCL_PIN, GPIO_FUNC_I2C);
  gpio_pull_up(PICO_DEFAULT_I2C_SDA_PIN);
  gpio_pull_up(PICO_DEFAULT_I2C_SCL_PIN);
  lcd_init();

  // Initial State
  handleEncoder(&rotaryState);

  absolute_time_t readTime = make_timeout_time_ms(TIME_READ);

  while (true) {
    if ( time_reached(readTime) ) {
      rotaryState.potValue = adc_read();
      char buffer[6];
      sprintf(buffer, "%d", rotaryState.potValue);
      lcd_set_cursor(1, 0);
      lcd_string("     ");
      lcd_set_cursor(1, 0);
      lcd_string(buffer);
      readTime = make_timeout_time_ms(TIME_READ);
    }
    // Get the movement of the rotary encoder
    if (rotaryEncoder)
    {
      rotaryState.rotationValue = checkRotaryEncoder();
      if (rotaryState.rotationValue !=0) handleEncoder(&rotaryState);
    }
 
  }
}

void handleLEDOnTime() {
  lcd_clear();
  lcd_set_cursor(0, 0);
  lcd_string(msg[0]);
}
void handleLEDIntensity() {
  lcd_clear();
  lcd_set_cursor(0, 0);
  lcd_string(msg[1]);
}

void handleLightThreshold() {
  lcd_clear();
  lcd_set_cursor(0, 0);
  lcd_string(msg[2]);
}

void handleExitSetup() {
  lcd_clear();
  lcd_set_cursor(0, 0);
  lcd_string(msg[3]);
}

void handleEncoder(State* rotaryState) {
  uint32_t direction;
  typedef struct {
    uint32_t newState[4][3];
    void (*fun_ptr[4])();
  } stateTable;

  const stateTable rotaryStateTable = {
{
    //Initial Rotation CW   Rotatation CCW
       {0,        1,           3},
       {0,        2,           0},
       {0,        3,           1},
       {0,        0,           2}
  },
  {&handleLEDOnTime,
   &handleLEDIntensity,
   &handleLightThreshold,
   &handleExitSetup}
  };
                          
  if (rotaryState->rotationValue == 1) direction = CW;
  else if (rotaryState->rotationValue == -1) direction = CCW;
  else direction = 0;
  rotaryState->state = rotaryStateTable.newState[rotaryState->state][direction];
  rotaryStateTable.fun_ptr[rotaryState->state]();
}