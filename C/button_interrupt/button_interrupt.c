 /* Call an interrupt when a button is presseed */

#include <stdio.h>
#include <stdint.h>
#include "pico/stdlib.h"
#include "pico/sleep.h"
#include "hardware/clocks.h"
#include "hardware/rosc.h"
#include "hardware/structs/scb.h"
#include "hardware/adc.h"

const uint32_t EDGE_FALL = 0x4;
const uint32_t EDGE_RISE = 0x8;
const bool OUTPUT = true;
const bool INPUT = false;
const bool HIGH = true;
const bool LOW = false;

void recover_from_sleep(uint scb_orig, uint clock0_orig, uint clock1_orig){

    //Re-enable ring Oscillator control
    rosc_write(&rosc_hw->ctrl, ROSC_CTRL_ENABLE_BITS);

    //reset procs back to default
    scb_hw->scr = scb_orig;
    clocks_hw->sleep_en0 = clock0_orig;
    clocks_hw->sleep_en1 = clock1_orig;

    //reset clocks
    clocks_init();
    stdio_init_all();

    return;
}

void measure_freqs(void) {
    uint f_pll_sys = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_PLL_SYS_CLKSRC_PRIMARY);
    uint f_pll_usb = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_PLL_USB_CLKSRC_PRIMARY);
    uint f_rosc = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_ROSC_CLKSRC);
    uint f_clk_sys = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_CLK_SYS);
    uint f_clk_peri = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_CLK_PERI);
    uint f_clk_usb = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_CLK_USB);
    uint f_clk_adc = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_CLK_ADC);
    uint f_clk_rtc = frequency_count_khz(CLOCKS_FC0_SRC_VALUE_CLK_RTC);

    printf("pll_sys  = %dkHz\n", f_pll_sys);
    printf("pll_usb  = %dkHz\n", f_pll_usb);
    printf("rosc     = %dkHz\n", f_rosc);
    printf("clk_sys  = %dkHz\n", f_clk_sys);
    printf("clk_peri = %dkHz\n", f_clk_peri);
    printf("clk_usb  = %dkHz\n", f_clk_usb);
    printf("clk_adc  = %dkHz\n", f_clk_adc);
    printf("clk_rtc  = %dkHz\n", f_clk_rtc);
    uart_default_tx_wait_blocking();
    // Can't measure clk_ref / xosc as it is the ref
}

void adc_setup(uint adc_channel) {
    int adc_gpio[3] = {26, 27, 28};
    adc_init();
    // Make sure GPIO is high-impedance, no pullups etc
    adc_gpio_init(adc_gpio[adc_channel]);
    // Select which channel to read
    adc_select_input(adc_channel);
}

int main() {
    const uint ADC_GPIO = 28;
    const uint ADC_INPUT = 2;
    const uint buttonPin = 17;
    const uint ledPin = 12;
    const uint adcTurnOnPin = 16;
    const uint16_t lightLevelThreshold = 300;
    const float conversion_factor = 3.3f / (1 << 12);

    gpio_init(buttonPin); 
    gpio_set_dir(buttonPin, GPIO_IN);
    gpio_pull_up(buttonPin);
    gpio_init(ledPin);
    gpio_set_dir(ledPin, GPIO_OUT);
    gpio_init(adcTurnOnPin);
    gpio_set_dir(adcTurnOnPin, GPIO_OUT);
    stdio_init_all();
    //save values for later
    uint scb_orig = scb_hw->scr;
    uint clock0_orig = clocks_hw->sleep_en0;
    uint clock1_orig = clocks_hw->sleep_en1;
    gpio_put(adcTurnOnPin, HIGH);
    adc_setup(ADC_INPUT);
 //   printf("Frequencies before sleep\n");
 //   measure_freqs();
  
  while(true) {
//      printf("Running from XOSC\n");
//      uart_default_tx_wait_blocking();
      sleep_run_from_xosc();
//     printf("Going to Sleep\n");
//      uart_default_tx_wait_blocking();
      sleep_goto_dormant_until_pin(buttonPin, true, false);
//      printf("Button Pressed\n");
//      printf("****Clocks After Sleep****\n");
//      measure_freqs();
      recover_from_sleep(scb_orig, clock0_orig, clock1_orig);
     //clocks should be restored
//      printf("****Clocks after reset****\n");
//      measure_freqs();
      gpio_put(adcTurnOnPin, HIGH);
      adc_setup(ADC_INPUT);
      // Take ADC Reading
      // 12-bit conversion, assume max value == ADC_VREF == 3.3 V
      uint16_t result = adc_read();
//      printf("****ADC Reading****\n");
//      printf("Raw value: %d, voltage: %f V\n\n", result, result * conversion_factor);
//      uart_default_tx_wait_blocking();
      gpio_put(adcTurnOnPin, LOW);
      if (result < lightLevelThreshold) {
          gpio_put(ledPin, HIGH);
          sleep_ms(10000);
          gpio_put(ledPin, LOW);
     }
    }
}
