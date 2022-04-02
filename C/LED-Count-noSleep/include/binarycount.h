const uint32_t LED_PIN_MAX = 11;
const uint32_t LED_PIN_MIN = 8;
const uint RESET_BUTTON = 16;
typedef struct {uint32_t count;
                absolute_time_t tToggle;
                uint32_t mask;
                const uint32_t delayTime;} count_t;

gpio_irq_callback_t button_interrupt_callback(uint, uint32_t);
void increment(count_t *);
void reset(count_t *);
