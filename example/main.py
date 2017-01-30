import utime as time
import usocket as socket


PIN_NUM = 2
NUM_LEDS = 8
SLEEP_TIME = 10
HOST = 'kojistatus-hroncok.rhcloud.com'
USERNAME = 'churchyard'
BRIGHTNES = 7  # 0-255


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


def bright(r, g, b):
    div = sum((r, g, b)) / BRIGHTNES
    return tuple(int(i) for i in (r / div, g / div, b / div))


COLORS = {
    'free': bright(0, 0, 255),
    'open': bright(255, 255, 0),
    'failed': bright(255, 0, 0),
    'canceled': bright(30, 30, 30),
    'closed': bright(0, 255, 0),
}


def last_colors(num):
    ai = socket.getaddrinfo(HOST, 80)
    addr = ai[0][-1]
    for idx, line in enumerate(download_status(addr)):
        if idx == num:
            break
        _, status = line.split()
        yield COLORS[status]


def leds_off(write=False):
    for led in range(NUM_LEDS):
        np[led] = (0, 0, 0)
    if write:
        np.write()


try:
    import network
except ImportError:
    pass
else:
    wlan = network.WLAN(network.STA_IF)
    counter = 0
    while not wlan.isconnected():
        leds_off()
        np[counter] = bright(0, 0, 255)
        np.write()
        counter += 1
        counter %= NUM_LEDS
        time.sleep(1)
    leds_off(write=True)


while True:
    try:
        for led, color in enumerate(last_colors(NUM_LEDS)):
            np[led] = color
        np.write()
    except:
        pass
    time.sleep(SLEEP_TIME)
