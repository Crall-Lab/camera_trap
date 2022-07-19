import datetime
import logging
import os
import subprocess
import time

import adafruit_aw9523
import board
import digitalio
#import picamera2

# led pins and currents are defined in a separate file
import led_driver

logging.basicConfig(
    level=logging.INFO,
    filename='capture.log')

images_dir = os.path.expanduser('~/images')

# seconds to wait after turning on LEDs and before taking a picture
pre_capture_delay = 60 * 5
#pre_capture_delay = 1
# seconds to wait after taking picture
post_capture_delay = 60 * 5
#post_capture_delay = 1
# seconds to wait after starting camera to allow it to 'settle'
camera_capture_delay = 1.0
# if capture takes more than capture_timeout seconds, error out
capture_timeout = 5.0


def capture(color, ir_led):
    # generate filename
    dts = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    fn = os.path.join(images_dir, f'{dts}_{color}.jpg')

    # turn on IR light
    ir_led.turn_on()

    # take picture
    timeout = camera_capture_delay * 1000
    cmd = f"libcamera-still -t {timeout:g} -o {fn}"
    try:
        subprocess.check_call(cmd.split(), timeout=capture_timeout)
    except Exception as e:
        logging.error("capture failed with error: %s" % e)
    # with picamera2.Picamera2() as cam:
    #     cam.start_preview(picamera2.Preview.NULL)
    #     preview_config = cam.create_preview_configuration()
    #     still_config = cam.create_still_configuration()
    #     cam.configure(preview_config)
    #     cam.start()
    #     # TODO is it necessary to delay to allow the camera settings to settle?
    #     time.sleep(camera_capture_delay)
    #     cam.switch_mode_and_capture_file(still_config, fn)
    #     cam.stop()

    # turn off IR light
    ir_led.turn_off()


if __name__ == '__main__':
    leds = led_driver.create_leds()

    cycle = ['green', 'blue', 'uv']
    cycle_index = 0

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    logging.info(f"Saving images to {images_dir}")

    while True:
        try:
            color = cycle[cycle_index % len(cycle)]
            logging.info(f"Cycle {cycle_index} {color}")
            leds[color].turn_on()
            time.sleep(pre_capture_delay)
            try:
                capture(color, leds['ir'])
            except Exception as e:
                logging.error("Capture error: %s" % e)
                pass
            leds[color].turn_off()
            # TODO instead of setting post_capture, use a fixed period
            time.sleep(post_capture_delay)
            cycle_index += 1
        except Exception as e:
            logging.error("Cycle error: %s" % e)
            for color in leds:
                leds[color].turn_off()
