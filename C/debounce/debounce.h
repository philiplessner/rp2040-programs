// Public interfac
typedef struct {
uint32_t button;
uint16_t state;
volatile bool switchFlag;
int32_t ms_delay;
struct repeating_timer *timer;
}Debounce;

// Public functions
void debounce_init(Debounce* const self, 
                   uint32_t button, 
                   int32_t ms_delay);
bool debounce_getFlag(Debounce* const self);
void debounce_disableTimerISR(Debounce* const self);
void debounce_enableTimerISR(Debounce* const self);