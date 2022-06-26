import adafruit_aw9523
import board
import digitalio


i2c = board.I2C()
aw = adafruit_aw9523.AW9523(i2c)
aw.LED_modes = 0xFF
aw.directions = 0xFF
[aw.set_constant_current(pin, 0) for pin in range(16)]
