import datetime
import time

import board
import digitalio
import adafruit_aw9523


# seconds to wait after turning on LEDs and before taking a picture
pre_capture_delay = 60 * 5
pre_capture_delay = 1
# seconds to wait after taking picture
post_capture_delay = 60 * 5
post_capture_delay = 1

# aw9523 max current is 37 ma
# 255 = max
ma_to_units = lambda ma: int(ma / 37.0 * 255)


class LEDBank:
    def __init__(self, aw, pins, current_ma=20):
        self.aw = aw
        self.pins = pins
        self.leds = []
        for pin in self.pins:
            led = self.aw.get_pin(pin)
            led.switch_to_output(value=True)
            self.leds.append(led)
        self.set_current_ma(current_ma)

    def set_current_ma(self, ma):
        self.current_units = ma_to_units(ma)
        for pin in self.pins:
            self.aw.set_constant_current(pin, self.current_units)

    def turn_on(self):
        for led in self.leds:
            led.value = False

    def turn_off(self):
        for led in self.leds:
            led.value = True


def capture(color):
    # generate filename
    # take picture
    pass


if __name__ == '__main__':
    i2c = board.I2C()
    aw = adafruit_aw9523.AW9523(i2c)

    leds = {
        'green': LEDBank(aw, [0, 1]),
        'blue': LEDBank(aw, [2, 3]),
        'uv': LEDBank(aw, [4, 5, 6, 7], 30),
    }

    cycle = ['green', 'blue', 'uv']
    cycle_index = 0

    while True:
        color = cycle[cycle_index % len(cycle)]
        print(f"Cycle {cycle_index} {color}")
        leds[color].turn_on()
        time.sleep(pre_capture_delay)
        capture(color)
        leds[color].turn_off()
        time.sleep(post_capture_delay)
        cycle_index += 1
