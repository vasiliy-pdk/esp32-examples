from machine import Pin, TouchPad

LED_PIN_NUMBER = 5  # Each board has a pin that is connected to the LED, you can find it by reading labels on your board
LED_ON = 0
LED_OFF = 1

# This number may differ from board to board. ESP32 datasheet https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf
# states that the GPIOs: 0, 2, 4, 27, 32; MTDO, MTCK, MTDI, MTMS support the touch.
#
# I've tried the pin 32 on Wemos Lolin 32 and that worked for me. It will also work for Wemos Lolin D32 and D32 Pro
TOUCH_PIN_NUMBER = 32
TOUCH_DETECTION_THRESHOLD = 600

touch_pad = TouchPad(Pin(TOUCH_PIN_NUMBER))
led_pin = Pin(LED_PIN_NUMBER, Pin.OUT)
led_pin.value(LED_OFF)


def light_led_on_touch(led, touch):
    sensor_value = touch.read()
    if sensor_value < TOUCH_DETECTION_THRESHOLD:
        led_state = LED_ON
    else:
        led_state = LED_OFF

    led.value(led_state)
    print("SENSOR VALUE: {value:4d}; LED PIN VALUE: {state:1d}".format(value=sensor_value, state=led_state))


while True:
    light_led_on_touch(led_pin, touch_pad)