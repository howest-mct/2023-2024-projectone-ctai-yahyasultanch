import time
# import py_neopixel_spidev as neopixel
from lib import neopixel_spidev as neopixel

# Init 8 LEDs on SPI bus 0, cs 0 with colors ordered green, red, blue
with neopixel.NeoPixelSpiDev(0, 0, n=8, pixel_order=neopixel.GRB) as pixels:
    try:
        # Set all pixels to white (R=255, G=255, B=255)
        pixels.fill(255 << 16 | 255 << 8 | 255)
        pixels.show()

        # Keep the LEDs on for a while
        time.sleep(10)

    except KeyboardInterrupt:
        pass
