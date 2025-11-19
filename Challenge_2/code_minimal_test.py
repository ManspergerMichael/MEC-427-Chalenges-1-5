"""Minimal test to verify basic CPX functionality"""

import time
import board
import touchio
from adafruit_circuitplayground import cp

# Test 1: Can we initialize one touch pad?
print("Test 1: Initializing A1...")
try:
    touch_pad = touchio.TouchIn(board.A1)
    print("A1 OK")
except Exception as e:
    print("A1 FAILED:", e)

# Test 2: Can we initialize A3?
print("Test 2: Initializing A3...")
try:
    touch_pad_a3 = touchio.TouchIn(board.A3)
    print("A3 OK")
except Exception as e:
    print("A3 FAILED:", e)

# Test 3: Can we initialize A5?
print("Test 3: Initializing A5...")
try:
    touch_pad_a5 = touchio.TouchIn(board.A5)
    print("A5 OK")
except Exception as e:
    print("A5 FAILED:", e)

# Flash green to show we got here
cp.pixels.brightness = 0.3
for _ in range(3):
    cp.pixels.fill((0, 100, 0))
    time.sleep(0.2)
    cp.pixels.fill((0, 0, 0))
    time.sleep(0.2)

print("All tests complete!")
