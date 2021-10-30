/**  
 * Controlling the Pi Pico GPIO with direct register access (SIO registers + IO Bank 0 registers)
 * 
 * Code example from the Raspberry Pi Pico Deep Pico - The Deep Dive course:
 * https://hackaday.io/course/178733-raspberry-pi-pico-and-rp2040-the-deep-dive
 */
#include <stdint.h>
#include "pico/stdlib.h"
#define MEM32(address) (*(volatile uint32_t *) (address))
#define GPIO_OE MEM32(SIO_BASE + SIO_GPIO_OE_OFFSET)
#define GPIO_OUT_REG MEM32(SIO_BASE + SIO_GPIO_OUT_OFFSET)
#define GPIO_TOGL MEM32(SIO_BASE + SIO_GPIO_OUT_XOR_OFFSET)
#define TIMER_REG(offset) MEM32(TIMER_BASE + offset)
#define TIMELR TIMER_REG(TIMER_TIMELR_OFFSET)
#define ALARM1 TIMER_REG(TIMER_ALARM1_OFFSET)
#define ARMED TIMER_REG(TIMER_ARMED_OFFSET)
#define EXT_LED 15
#define LED_BUILTIN PICO_DEFAULT_LED_PIN
// Macro to set nth-bit
/* 
     Set single bit at pos to '1' by generating a mask
     in the proper bit location and ORing (|) x with the mask. 
*/
#define SET_BIT(x, pos) (x |= (1U << pos))
// Macro to check nth-bit
/*
    Set single bit at pos to '1' by generating a mask
    in the proper bit location and Anding x with the mask.
    It evaluates 1 if a bit is set otherwise 0.
*/
#define CHECK_BIT(x, pos) (x & (1UL << pos))

/* Enables the SIO function for the given pin, by writing to the relevant CTRL register.
   (e.g. GPIO0_CTRL at 0x40014004) */
void enable_sio(int pin) {
    uint32_t *PIN_CTRL_REG = (uint32_t*)IO_BANK0_BASE + pin * 2 + 1;
    *PIN_CTRL_REG = GPIO_FUNC_SIO; // 5 = SIO function
}

void timerDelay(uint32_t microseconds) {
    ALARM1 = TIMELR + microseconds;
    // Bit 1 of the ARMED Register will be reset to 0 when ALARM1 fires
    while (CHECK_BIT(ARMED, 1));
}

int main() {
  // Enable the SIO function for GPIO 25 (built in LED) and GPIO 15 (external LED)
    enable_sio(EXT_LED);
    enable_sio(LED_BUILTIN);
    
  // Enable output on pin 25 and 15
  // sio_hw->gpio_oe points to 0xd0000020 (GPIO_OE)
    GPIO_OE = SET_BIT(GPIO_OE, EXT_LED);
    GPIO_OE = SET_BIT(GPIO_OE, LED_BUILTIN);
  // Set initial pin pattern
  // sio_hw->gpio_out points to 0xd0000010 (GPIO_OUT)
    GPIO_OUT_REG = SET_BIT(GPIO_OUT_REG, EXT_LED);
    GPIO_OUT_REG = SET_BIT(GPIO_OUT_REG, LED_BUILTIN);

    while (true) {
  // sio_hw->gpio_togl points to 0xd000001c (GPIO_OUT_XOR)
        GPIO_TOGL = (1<<EXT_LED) | (1<<LED_BUILTIN);
        timerDelay(100000);
    }
}

