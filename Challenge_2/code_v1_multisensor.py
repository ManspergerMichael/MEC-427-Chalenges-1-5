"""Version 1: Multi-sensor initialization only (A1, A3, A5)"""

import time
import board
import touchio
from adafruit_circuitplayground import cp

# Initialize three non-adjacent touch pads
touch_pads = [
    touchio.TouchIn(board.A1),
    touchio.TouchIn(board.A3),
    touchio.TouchIn(board.A5),
]

# Settings
PIXEL_COUNT = 10
BAR_COLOR = (255, 160, 0)
THRESHOLD_COLOR = (255, 255, 255)

cp.pixels.brightness = 0.3
cp.pixels.fill((0, 0, 0))

# Simple calibration - just first pad for now
cp.pixels[0] = (255, 140, 0)
samples = []
for _ in range(40):
    samples.append(touch_pads[0].raw_value)
    time.sleep(0.05)

samples.sort()
dry_baseline = samples[len(samples) // 2]

default_margin = 1000
threshold_margin = default_margin
detection_threshold = dry_baseline + threshold_margin

cp.pixels[0] = (0, 0, 0)

# State
wet_count = 0
dry_count = 0
is_wet = False

prev_btn_a = False
prev_btn_b = False

BAR_SPAN_COUNTS = 2000
MARGIN_STEP_COUNTS = 100


def clamp_int(value, lo, hi):
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def draw_bar_graph(raw_value, baseline, margin):
    delta = raw_value - baseline
    delta = clamp_int(delta, 0, BAR_SPAN_COUNTS)
    level = int((delta * PIXEL_COUNT) / BAR_SPAN_COUNTS)
    
    m = clamp_int(margin, 0, BAR_SPAN_COUNTS)
    t_idx = int((m * PIXEL_COUNT) / BAR_SPAN_COUNTS)
    if t_idx >= PIXEL_COUNT:
        t_idx = PIXEL_COUNT - 1
    
    for i in range(PIXEL_COUNT):
        if i == t_idx:
            cp.pixels[i] = THRESHOLD_COLOR
        elif i < level:
            cp.pixels[i] = BAR_COLOR
        else:
            cp.pixels[i] = (0, 0, 0)


while True:
    # Read only first pad for now
    raw_value = touch_pads[0].raw_value
    
    # Simple detection
    if raw_value > detection_threshold:
        wet_count = min(wet_count + 1, 3)
        dry_count = 0
    else:
        dry_count = min(dry_count + 1, 3)
        wet_count = 0
    
    new_is_wet = wet_count >= 2
    if new_is_wet != is_wet:
        is_wet = new_is_wet
    
    draw_bar_graph(raw_value, dry_baseline, threshold_margin)
    cp.red_led = is_wet
    
    # Button controls
    btn_a_pressed = cp.button_a
    btn_b_pressed = cp.button_b
    
    if btn_a_pressed and not prev_btn_a:
        new_margin = threshold_margin - MARGIN_STEP_COUNTS
        threshold_margin = clamp_int(new_margin, 0, 8000)
        detection_threshold = dry_baseline + threshold_margin
        cp.pixels[0] = (0, 50, 0)
    
    if btn_b_pressed and not prev_btn_b:
        new_margin = threshold_margin + MARGIN_STEP_COUNTS
        threshold_margin = clamp_int(new_margin, 0, 8000)
        detection_threshold = dry_baseline + threshold_margin
        cp.pixels[0] = (0, 50, 0)
    
    prev_btn_a = btn_a_pressed
    prev_btn_b = btn_b_pressed
    
    time.sleep(0.06)
