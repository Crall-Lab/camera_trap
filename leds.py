import argparse

import adafruit_aw9523
import board
import digitalio


ir_led_pin = 11

color_pins = {
    'green': [14, ],
    'blue': [1, ],
    'uv': [4, 7],
}

color_currents = {
    'green': 20,
    'blue': 20,
    'uv': 30,
}


# aw9523 max current is 37 ma
# 255 = max
ma_to_units = lambda ma: int(ma / 37.0 * 255)


class LEDBank:
    def __init__(self, aw, pins, current_ma=20):
        self.aw = aw
        self.pins = pins
        for pin in self.pins:
            mask = 0x1 << pin
            self.aw.LED_modes |= mask
            self.aw.directions |= mask
        self.current_ma = current_ma
        self.turn_off()

    def _write_current_ma(self, ma):
        self.current_units = ma_to_units(ma)
        for pin in self.pins:
            self.aw.set_constant_current(pin, self.current_units)

    def turn_on(self):
        self._write_current_ma(self.current_ma)

    def turn_off(self):
        self._write_current_ma(0)


class LEDPin:
    def __init__(self, aw, pin):
        self.pin = aw.get_pin(pin)
        self.pin.switch_to_output(value=False)
        self.turn_off()

    def turn_on(self):
        self.pin.value = True

    def turn_off(self):
        self.pin.value = False



def create_leds():
    i2c = board.I2C()
    aw = adafruit_aw9523.AW9523(i2c)

    leds = {}
    for color in color_pins:
        leds[color] = LEDBank(aw, color_pins[color], color_currents[color])
        leds[color].turn_off()

    leds['ir'] = LEDPin(aw, ir_led_pin)
    leds['ir'].turn_off()

    return leds


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Turn off all leds, options can be used to turn on specific leds")
    parser.add_argument(
        '-i', '--ir', default=None, type=bool,
        help='set state of ir led to on[1]/off[0]')
    for color in color_pins:
        parser.add_argument(
            '-%s' % color[0],
            '--%s' % color,
            default=None, type=bool,
            help='set state of %s led to on[1]/off[0]' % color)

    args = parser.parse_args()

    leds = create_leds()

    for color in leds:
        state = getattr(args, color)
        if state is not None:
            if state:
                leds[color].turn_on()
            else:
                leds[color].turn_off()
