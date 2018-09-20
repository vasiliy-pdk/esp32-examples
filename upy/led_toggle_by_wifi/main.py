import led
import server
import config

def start(ssid, password):
    server.init(ssid, password, handle_request)


html = """
<!DOCTYPE html>
<html>
    <head><title>ESP32 led status</title> </head>
    <body> 
      <h1>Led is %s</h1>
      <form method="POST">
        <button type="submit">Toggle the led!</button>
      </form>
    </body>
</html>
"""


def handle_request(method, uri):
    root_uri = '/'
    if uri != root_uri:
        return ''

    print('Handling request {} {}'.format(method, uri))

    if method == 'POST':
        led.toggle()

    led_status = 'Off'
    if led.is_on():
        led_status = 'On'

    response = html % led_status
    return response


if len(config.SSID):
    start(config.SSID, config.PASSWORD)