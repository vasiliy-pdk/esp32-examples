import utime
from machine import Pin

LED_PIN_NUMBER = 5
LED_ON = 0
LED_OFF = 1

led_pin = Pin(LED_PIN_NUMBER, Pin.OUT)

while True:
  print('Blinking...')
  led_pin.value(LED_ON)
  utime.sleep_ms(500)
  led_pin.value(LED_OFF)
  utime.sleep_ms(500)
