import time

import picamera2


# TODO argparse for settings (frame delay, save image, etc)

cam = picamera2.Picamera2()
cam.start_preview(picamera2.Preview.NULL)

preview_config = cam.create_preview_configuration()
cam.configure(preview_config)

cam.start()

focus_max = 1

while True:
    try:
        meta = cam.capture_metadata()
        focus = meta['FocusFoM']

        focus_max = max(focus_max, focus)

        # -----*------| (focus/focus_max)
        chars_per_unit = min(1, 80 / focus_max)
        s = '-' * int(focus * chars_per_unit) + '*'
        if focus != focus_max:
            s = s.ljust(int(focus_max * chars_per_unit), '-') + '|'
        s += ' %s/%s' % (focus, focus_max)
        print(s)
        #print("Focus %s" % meta['FocusFoM'])
        #print(meta)
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

# save final image
cam.capture_file("focus.jpg")

cam.stop()
