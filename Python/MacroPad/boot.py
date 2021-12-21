import storage
import board, digitalio
# The mute/unmute button is wired to connect GP0 to GND when pushed.
button = digitalio.DigitalInOut(board.GP0)
button.pull = digitalio.Pull.UP
# Press mute/unmute button while plugging in device to have CircuitPy drive appear
if button.value:
    storage.disable_usb_drive()