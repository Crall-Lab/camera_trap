import datetime
import os
import time

import adafruit_aw9523
import board
import digitalio
import picamera2


images_dir = os.path.expanduser('~/images')

IR_LED_PIN = 11

# seconds to wait after turning on LEDs and before taking a picture
pre_capture_delay = 60 * 5
pre_capture_delay = 1
# seconds to wait after taking picture
post_capture_delay = 60 * 5
post_capture_delay = 1
# seconds to wait after starting camera to allow it to 'settle'
camera_capture_delay = 1.0

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


def capture(color, ir_led):
    # generate filename
    dts = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    fn = os.path.join(images_dir, f'{dts}_{color}.jpg')

    # turn on IR light
    ir_led.value = True

    # take picture
    with picamera2.Picamera2() as cam:
        cam.start_preview(picamera2.Preview.NULL)
        preview_config = cam.preview_configuration()
        still_config = cam.still_configuration()
        cam.configure(preview_config)
        cam.start()
        # TODO is it necessary to delay to allow the camera settings to settle?
        time.sleep(camera_capture_delay)
        cam.switch_mode_and_capture_file(still_config, fn)
        cam.stop()

    # turn off IR light
    ir_led.value = False


if __name__ == '__main__':
    i2c = board.I2C()
    aw = adafruit_aw9523.AW9523(i2c)

    leds = {
        'green': LEDBank(aw, [14, ]),
        'blue': LEDBank(aw, [1, ]),
        'uv': LEDBank(aw, [4, 7], 30),
    }

    ir_led = aw.get_pin(IR_LED_PIN)
    ir_led.switch_to_output(value=False)

    cycle = ['green', 'blue', 'uv']
    cycle_index = 0

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    print(f"Saving images to {images_dir}")

    while True:
        color = cycle[cycle_index % len(cycle)]
        print(f"Cycle {cycle_index} {color}")
        leds[color].turn_on()
        time.sleep(pre_capture_delay)
        capture(color, ir_led)
        leds[color].turn_off()
        # TODO instead of setting post_capture, use a fixed period
        time.sleep(post_capture_delay)
        cycle_index += 1
