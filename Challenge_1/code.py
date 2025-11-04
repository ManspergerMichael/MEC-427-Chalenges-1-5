import time

import board
import touchio
from adafruit_circuitplayground import cp

# Initialize the capacitive touch sensor on A1
touch_pad = touchio.TouchIn(board.A1)

# Set up some initial variables
threshold = 2500  # Ambient ~1700, water ~3250
led_index = 0    # Which NeoPixel to light up

# Initialize NeoPixels
cp.pixels.brightness = 0.3  # Set brightness to 30%
cp.pixels.fill((0, 0, 0))  # Turn all pixels off initially

while True:
    # Read the capacitive touch value
    if touch_pad.raw_value > threshold:
        print("Water detected!")
        # Light up the NeoPixel in blue
        cp.pixels[led_index] = (0, 0, 255)
    else:
        print("No water detected")
        # Turn off the NeoPixel
        cp.pixels[led_index] = (0, 0, 0)

    # Print the raw value for calibration purposes
    print(f"Raw capacitive value: {touch_pad.raw_value}")

    # Small delay to prevent overwhelming the serial console
    time.sleep(0.1)
    time.sleep(0.1)
    time.sleep(0.1)
