from machine import Pin

LED_PIN_NUMBER = 5  # Each board has a pin that is connected to the LED, you can find it by reading labels on your board
LED_ON = 0
LED_OFF = 1

led_pin = Pin(LED_PIN_NUMBER, Pin.OUT)


def toggle():
    if is_on():
        off()
    else:
        on()


def off():
    led_pin.value(LED_OFF)


def on():
    led_pin.value(LED_ON)


def is_on():
    return led_pin.value() == LED_ON