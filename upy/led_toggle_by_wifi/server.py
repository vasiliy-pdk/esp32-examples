import network  # network documentation is available here
                # https://docs.micropython.org/en/latest/esp8266/library/network.html#module-network
import socket
import utime


def init(ssid, password, handler):
    print('Initializing server on the board...')
    nic = network.WLAN(network.STA_IF)  # STA_IF means client that connects to other access points
    ip_address = connect(nic, ssid, password)
    if ip_address:
        init_socket(ip_address, handler)


def connect(nic, ssid, password):
    print('Connecting to {}'.format(ssid))
    nic.active(True)
    nic.connect(ssid, password)

    have_slept = 0
    while have_slept <= 10 and not nic.isconnected():
        utime.sleep(1)
        have_slept += 1
        status = nic.status()
        if status != network.STAT_CONNECTING:
            print('Failed to connect with status {}. Reconnecting...'.format(status))
        else:
            print('Still connecting...')

    if nic.status() == network.STAT_GOT_IP:
        ip_address = nic.ifconfig()[0]
        return ip_address
    else:
        print('Failed to connect to the access point')
        list_available_access_points(nic)
        nic.disconnect()
        nic.active(False)
        return False


def list_available_access_points(nic):
    print('Available access points near you:')
    for ap_info in nic.scan():
        print(ap_info[0])


def init_socket(ip_address, handler):
    s = socket.socket()
    address = socket.getaddrinfo(ip_address, 80)[0][-1]
    s.bind(address)
    s.listen(1)
    print('Server is accessible on http://{}/'.format(ip_address))

    while True:
        handle_requests(s, handler)


def handle_requests(s, handler):
    client, client_address = s.accept()
    print('client connected from', client_address)
    request = extract_request_params(client)
    sent_bytes = False

    if request:
        response = handler(request["method"], request["uri"])
        response_length = len(response)
        if response_length > 0:
            client.send("HTTP/1.1 200 OK\r\n\r\n")
            sent_bytes = client.send(response)
            print('Response send {} all: {}'.format(sent_bytes, sent_bytes == response_length))

    if not sent_bytes:
        client.send("HTTP/1.1 400 BAD REQUEST\r\n")

    client.close()
    print('Socket closed')


def extract_request_params(client):
    client_file = client.makefile('rwb', 0)
    request_line = client_file.readline()

    # make sure that all request is read, not sure why but otherwise the response is not sent
    while True:
        line = client_file.readline()
        if not line or line == b'\r\n':
            break

    print('request line {}'.format(request_line))

    try:
        method, uri = request_line.decode().strip().split()[0:2]
        return {
            'method': method,
            'uri': uri
        }
    except:
        print('unknown request format')
        return False
