import config
import led
import server
import page


def start(ssid, password):
    server.init(ssid, password, handle_request)


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

    return page.render(led_status)


if len(config.SSID):
    start(config.SSID, config.PASSWORD)