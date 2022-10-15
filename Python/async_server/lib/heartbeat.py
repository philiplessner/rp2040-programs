import uasyncio as asyncio
from machine import Pin


async def heartbeat(tms):
    led = Pin("LED", Pin.OUT)
    while True:
        led.toggle()
        await asyncio.sleep_ms(tms)
