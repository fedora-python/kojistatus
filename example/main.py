import utime as time
import usocket as socket


PIN_NUM = 2
NUM_LEDS = 8
SLEEP_TIME = 30
HOST = 'kojistatus-hroncok.rhcloud.com'
USERNAME = None


try:
    from machine import Pin
    from neopixel import NeoPixel
    pin = Pin(PIN_NUM, Pin.OUT)
    np = NeoPixel(pin, NUM_LEDS)
except ImportError:
    # a real computer, no HW access

    class FakeNeoPixel(list):
        def __init__(self):
            super()
            for led in range(NUM_LEDS):
                self.append((0, 0, 0))

        def write(self):
            print(' '.join('{}'.format(c) for c in self))

    np = FakeNeoPixel()


PATH = USERNAME + '/' if USERNAME else ''


def download_status(addr):
    s = socket.socket()
    s.connect(addr)
    s.send(bytes(
        'GET /{} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(PATH, HOST), 'utf8'))
    data = ''
    while True:
        chunk = s.recv(100)
        if chunk:
            data += chunk.decode('utf-8')
        else:
            break
    s.close()

    head, body = data.split('\r\n\r\n', 2)

    yield from body.split('\n')


COLORS = {
    'free': (0, 0, 255 // 10),
    'open': (255 // 10, 255 // 10, 0),
    'failed': (255 // 10, 0, 0),
    'canceled': (127 // 10, 0, 0),
    'closed': (0, 255 // 10, 0),
}


def last_colors(num):
    ai = socket.getaddrinfo(HOST, 80)
    addr = ai[0][-1]
    for idx, line in enumerate(download_status(addr)):
        if idx == num:
            break
        _, status = line.split()
        yield COLORS[status]


time.sleep(20)  # Give it a time to connect
while True:
    try:
        for led, color in enumerate(last_colors(NUM_LEDS)):
            np[led] = color
        np.write()
    except:
        pass
    time.sleep(SLEEP_TIME)
