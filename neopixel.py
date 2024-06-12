# import time
# # import py_neopixel_spidev as neopixel
# from lib import neopixel_spidev as neopixel
# # Init 8 LEDs on SPI bus 0, cs 0 with colors ordered green, red, blue
# with neopixel.NeoPixelSpiDev(0, 0, n=8, pixel_order=neopixel.GRB) as pixels:
#     try:
#         while True: 
#             for i in range(8):
#                 pixels._set_item(i, 255,0,0,255)
#                 pixels.show()
#                 time.sleep(1)
#                 pixels.fill(0)
#                 time.sleep(0.5)
#                 # fill all colors with R 127, G 255, B 0
#                 pixels.fill( 127 << 16 | 255 << 8 | 0)
#     except KeyboardInterrupt:
#         pass

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
