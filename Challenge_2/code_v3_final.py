"""Version 3: Final - with EMA smoothing and debug output"""

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

# Per-pad calibration with more samples
cp.pixels[0] = (255, 140, 0)
sample_lists = [[], [], []]
CAL_SAMPLES = 120
for _ in range(CAL_SAMPLES):
    for i in range(3):
        sample_lists[i].append(touch_pads[i].raw_value)
    time.sleep(0.05)

# Calculate per-pad baselines
dry_baselines = []
for i in range(3):
    sample_lists[i].sort()
    dry_baselines.append(sample_lists[i][len(sample_lists[i]) // 2])

# Thresholds
default_margin = 1000
threshold_margin = default_margin
detection_thresholds = []
for b in dry_baselines:
    detection_thresholds.append(b + threshold_margin)

cp.pixels[0] = (0, 0, 0)

# State
wet_count = 0
dry_count = 0
is_wet = False

prev_btn_a = False
prev_btn_b = False

BAR_SPAN_COUNTS = 2000
MARGIN_STEP_COUNTS = 100

# Smoothing
SMOOTHING_ALPHA = 0.25
smoothed_values = [None, None, None]

# Debug
DEBUG = True


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
    # Read all pads
    raw_values = []
    for i in range(3):
        raw_values.append(touch_pads[i].raw_value)
    
    # Apply EMA smoothing
    for i in range(3):
        if smoothed_values[i] is None:
            smoothed_values[i] = raw_values[i]
        else:
            smoothed_values[i] = int(smoothed_values[i] * (1 - SMOOTHING_ALPHA) + raw_values[i] * SMOOTHING_ALPHA)
    
    # Use smoothed values
    for i in range(3):
        raw_values[i] = smoothed_values[i]
    
    # Use max for display
    raw_value = raw_values[0]
    if raw_values[1] > raw_value:
        raw_value = raw_values[1]
    if raw_values[2] > raw_value:
        raw_value = raw_values[2]
    
    # Check if any pad triggered
    any_triggered = False
    for i in range(3):
        if raw_values[i] > detection_thresholds[i]:
            any_triggered = True
            break
    
    if any_triggered:
        wet_count = min(wet_count + 1, 3)
        dry_count = 0
    else:
        dry_count = min(dry_count + 1, 3)
        wet_count = 0
    
    new_is_wet = wet_count >= 2
    if new_is_wet != is_wet:
        is_wet = new_is_wet
    
    # Debug output
    if DEBUG:
        deltas = []
        thr_lo = []
        thr_hi = []
        wet_per_pad = []
        for i in range(3):
            deltas.append(raw_values[i] - dry_baselines[i])
            thr_lo.append(dry_baselines[i] - threshold_margin)
            thr_hi.append(dry_baselines[i] + threshold_margin)
            wet_per_pad.append(raw_values[i] > detection_thresholds[i])
        
        print("r:", raw_values, "d:", deltas, "thr_lo:", thr_lo, "thr_hi:", thr_hi, "wet:", wet_per_pad, "maj:", is_wet, "margin:", threshold_margin)
    
    # Use min baseline for display
    display_baseline = dry_baselines[0]
    if dry_baselines[1] < display_baseline:
        display_baseline = dry_baselines[1]
    if dry_baselines[2] < display_baseline:
        display_baseline = dry_baselines[2]
    
    draw_bar_graph(raw_value, display_baseline, threshold_margin)
    cp.red_led = is_wet
    
    # Button controls
    btn_a_pressed = cp.button_a
    btn_b_pressed = cp.button_b
    
    if btn_a_pressed and not prev_btn_a:
        new_margin = threshold_margin - MARGIN_STEP_COUNTS
        threshold_margin = clamp_int(new_margin, 0, 8000)
        for i in range(3):
            detection_thresholds[i] = dry_baselines[i] + threshold_margin
        cp.pixels[0] = (0, 50, 0)
    
    if btn_b_pressed and not prev_btn_b:
        new_margin = threshold_margin + MARGIN_STEP_COUNTS
        threshold_margin = clamp_int(new_margin, 0, 8000)
        for i in range(3):
            detection_thresholds[i] = dry_baselines[i] + threshold_margin
        cp.pixels[0] = (0, 50, 0)
    
    prev_btn_a = btn_a_pressed
    prev_btn_b = btn_b_pressed
    
    time.sleep(0.06)
