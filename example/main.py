import utime as time
import usocket as socket


# User defined constants
PIN_NUM = 2
NUM_LEDS = 8
SLEEP_TIME = 10
PULSE_TIME = 0.15
HOST = 'vps.frenzy.cz'
PORT = 8080
USERNAME = 'churchyard'
BRIGHTNESS = 7  # 0-255
PULSE_BRIGHTNESS = 32  # 0-255; > BRIGHTNESS


# Calculated constants
PATH = USERNAME + '/' if USERNAME else ''
PULSE_SLEEP_TIME = PULSE_TIME / (2 * (PULSE_BRIGHTNESS - BRIGHTNESS))


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


def bright(rgb, brightness=BRIGHTNESS):
    r, g, b = rgb
    try:
        div = sum(rgb) / brightness
    except ZeroDivisionError:
        return (0, 0, 0)
    return tuple(int(i) for i in (r / div, g / div, b / div))


COLORS = {
    'free': (0, 0, 255),
    'open': (255, 255, 0),
    'failed': (255, 0, 0),
    'canceled': (30, 30, 30),
    'closed': (0, 255, 0),
}


def latest_builds(num):
    ai = socket.getaddrinfo(HOST, PORT)
    addr = ai[0][-1]
    for idx, line in enumerate(download_status(addr)):
        if idx == num:
            break
        taskid, status = line.split()
        yield int(taskid), status


def leds_off(write=False):
    for led in range(NUM_LEDS):
        np[led] = (0, 0, 0)
    if write:
        np.write()


def pulse(leds, colors):
    def inner(brightness):
        for color_idx, led in enumerate(leds):
            np[led] = bright(colors[color_idx], brightness)
        np.write()
        time.sleep(PULSE_SLEEP_TIME)

    for brightness in range(BRIGHTNESS, PULSE_BRIGHTNESS + 1):
        inner(brightness)
    for brightness in reversed(range(BRIGHTNESS, PULSE_BRIGHTNESS + 1)):
        inner(brightness)

    np.write()


try:
    import network
except ImportError:
    pass
else:
    wlan = network.WLAN(network.STA_IF)
    counter = 0
    while not wlan.isconnected():
        if not counter:
            leds_off()
        pulse((counter,), ((0, 0, 255),))
        counter += 1
        counter %= NUM_LEDS
        time.sleep(1)
    leds_off(write=True)


last = {}
while True:
    current = {}
    pulse_leds = []
    pulse_colors = []
    try:
        for led, build in enumerate(latest_builds(NUM_LEDS)):
            taskid, status = build
            current[taskid] = status
            color = bright(COLORS[status])
            if taskid not in last or last[taskid] != status:
                pulse_leds.append(led)
                pulse_colors.append(color)
            np[led] = color
        np.write()
        if pulse_leds:
            pulse(pulse_leds, pulse_colors)
        last = current
    except Exception:
        pass
    time.sleep(SLEEP_TIME)
