"""Three-probe capacitive water level voting sensor
with on-device calibration UI.

Challenge 2 objective:
Use three capacitive probes (A1, A2, A3) and majority voting (>=2 detect water)
for robust fluid level detection. A single failed / noisy probe is tolerated.

Features
- Per-probe auto-baseline on boot (~2 s) using median for robustness.
- Unified adjustable margin added to each baseline
    to form per-probe thresholds.
- Majority vote: if at least 2 of 3 probes read above
    their threshold (with debounce),
    the global detection state becomes True.
- NeoPixel bar visualizes the *maximum* delta above baseline among the probes;
    marker shows the adjustable margin position.
- Button A/B adjust the margin; hold A+B to save to cal.txt (shared margin).
- Red status LED indicates majority detection True.
"""

import time

import board
import touchio
from adafruit_circuitplayground import cp

# Initialize the capacitive touch sensors on A1, A2, A3
touch_pads = [
    touchio.TouchIn(board.A1),
    touchio.TouchIn(board.A2),
    touchio.TouchIn(board.A3),
]

# Settings for visualization and tuning
PIXEL_COUNT = 10
BAR_COLOR = (255, 160, 0)       # amber for bar
THRESHOLD_COLOR = (255, 255, 255)  # white marker (not flashing)

# Initialize NeoPixels
cp.pixels.brightness = 0.3
cp.pixels.fill((0, 0, 0))

# --- Auto-calibration on startup ---


def capture_baseline(pad):
    """Capture median baseline for a single touch pad over ~2 seconds."""
    readings = []
    for _ in range(40):  # ~2 seconds at 0.05s/sample
        readings.append(pad.raw_value)
        time.sleep(0.05)
    readings.sort()
    return readings[len(readings) // 2]


#
# Show amber pixel 0 while capturing baselines
cp.pixels[0] = (255, 140, 0)  # amber
dry_baselines = [capture_baseline(p) for p in touch_pads]
print("Baselines:", dry_baselines)

# Load saved margin if present (plain text to avoid needing the json module)
default_margin = 1000
threshold_margin = default_margin
try:
    with open("cal.txt", "r") as f:
        txt = f.read().strip()
        threshold_margin = int(txt)
except Exception:
    pass

# Per-probe low/high thresholds derived from baseline ± shared margin
thr_lo = [b - threshold_margin for b in dry_baselines]
thr_hi = [b + threshold_margin for b in dry_baselines]
print("Initial margin:", threshold_margin)
print("Initial thresholds lo/hi:", thr_lo, thr_hi)

# End of calibration indicator: turn off pixel 0 (no white flash)
cp.pixels[0] = (0, 0, 0)

# Debounce and UI state
wet_counts = [0, 0, 0]
dry_counts = [0, 0, 0]
probe_wet = [False, False, False]
majority_wet = False

prev_btn_a = False
prev_btn_b = False
ab_hold_started_at = None
a_hold_started_at = None
MARGIN_STEP_COUNTS = 100   # counts to change per button press
BAR_SPAN_COUNTS = 2000     # map 0..BAR_SPAN across the 10 pixels
REBASE_HOLD_SEC = 2.0       # hold A to re-capture baselines
AUTO_TRACK_AFTER_SEC = 3.0  # start slow baseline tracking after dry stable
AUTO_TRACK_MAX_DELTA = 50   # counts; dry stable threshold
dry_stable_started_at = None


def clamp_int(value, lo, hi):
    """Clamp integer value to [lo, hi]."""
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def draw_bar_graph(max_delta, margin):
    """Draw bar for max_delta above baseline and white threshold marker.

    max_delta: maximum (raw - baseline) among probes.
    margin:    shared adjustable margin.
    """
    d = clamp_int(max_delta, 0, BAR_SPAN_COUNTS)
    level = int((d * PIXEL_COUNT) / BAR_SPAN_COUNTS)  # 0..10

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
    # Read all probe raw values
    raw_values = [p.raw_value for p in touch_pads]

    # Per-probe hysteresis update (polarity-agnostic: trigger if beyond margin)
    for i in range(3):
        if (raw_values[i] > thr_hi[i]) or (raw_values[i] < thr_lo[i]):
            wet_counts[i] = min(wet_counts[i] + 1, 3)
            dry_counts[i] = 0
        else:
            dry_counts[i] = min(dry_counts[i] + 1, 3)
            wet_counts[i] = 0
        probe_wet[i] = wet_counts[i] >= 2

    # Majority vote (>=2 wet probes)
    majority_wet = (probe_wet.count(True) >= 2)

    # Visual bar uses maximum absolute delta among probes
    max_delta = max(
        abs(raw_values[i] - dry_baselines[i]) for i in range(3)
    )
    draw_bar_graph(max_delta, threshold_margin)

    # Serial output (throttled): raw values, deltas, wet flags, majority
    deltas = [raw_values[i] - dry_baselines[i] for i in range(3)]
    print(
        "r:", raw_values,
        "d:", deltas,
        "thr_lo:", thr_lo,
        "thr_hi:", thr_hi,
        "wet:", probe_wet,
        "maj:", majority_wet,
        "margin:", threshold_margin,
    )

    # Auto-track baselines when dry and stable for a while
    max_abs_delta = max(abs(x) for x in deltas)
    if (not majority_wet) and (max_abs_delta <= AUTO_TRACK_MAX_DELTA):
        if dry_stable_started_at is None:
            dry_stable_started_at = time.monotonic()
        elif time.monotonic() - dry_stable_started_at > AUTO_TRACK_AFTER_SEC:
            for i in range(3):
                dry_baselines[i] = int(
                    (dry_baselines[i] * 99 + raw_values[i]) / 100
                )
            thr_lo = [b - threshold_margin for b in dry_baselines]
            thr_hi = [b + threshold_margin for b in dry_baselines]
            print("auto-track baselines:", dry_baselines)
    else:
        dry_stable_started_at = None

    # Red LED indicates majority detection state
    cp.red_led = majority_wet

    # Button edge detection for tuning
    btn_a_pressed = cp.button_a
    btn_b_pressed = cp.button_b

    if btn_a_pressed and not prev_btn_a:
        threshold_margin = clamp_int(
            threshold_margin - MARGIN_STEP_COUNTS, 0, 8000
        )
        thr_lo = [b - threshold_margin for b in dry_baselines]
        thr_hi = [b + threshold_margin for b in dry_baselines]
        cp.pixels[0] = (0, 50, 0)  # dim green blink
        print("Margin dec ->", threshold_margin)
    if btn_b_pressed and not prev_btn_b:
        threshold_margin = clamp_int(
            threshold_margin + MARGIN_STEP_COUNTS, 0, 8000
        )
        thr_lo = [b - threshold_margin for b in dry_baselines]
        thr_hi = [b + threshold_margin for b in dry_baselines]
        cp.pixels[0] = (0, 50, 0)
        print("Margin inc ->", threshold_margin)

    # Long press A+B to save margin (write plain integer to cal.txt)
    if btn_a_pressed and btn_b_pressed:
        if ab_hold_started_at is None:
            ab_hold_started_at = time.monotonic()
        elif time.monotonic() - ab_hold_started_at > 1.0:
            try:
                with open("cal.txt", "w") as f:
                    f.write(str(int(threshold_margin)))
            except Exception:
                pass
            print("Margin saved:", threshold_margin)
            # Flash green across ring to confirm save
            for _ in range(2):
                for i in range(PIXEL_COUNT):
                    cp.pixels[i] = (0, 100, 0)
                time.sleep(0.15)
                for i in range(PIXEL_COUNT):
                    cp.pixels[i] = (0, 0, 0)
                time.sleep(0.1)
            ab_hold_started_at = None
        # cancel A-only hold when both are down
        a_hold_started_at = None
    else:
        ab_hold_started_at = None
        # Long-press A to re-capture baselines
        if btn_a_pressed and (not btn_b_pressed):
            if a_hold_started_at is None:
                a_hold_started_at = time.monotonic()
            elif time.monotonic() - a_hold_started_at > REBASE_HOLD_SEC:
                # show amber while capturing
                cp.pixels.fill((80, 40, 0))
                dry_baselines = [capture_baseline(p) for p in touch_pads]
                thr_lo = [b - threshold_margin for b in dry_baselines]
                thr_hi = [b + threshold_margin for b in dry_baselines]
                print("Recalibrated baselines:", dry_baselines)
                print("New thresholds lo/hi:", thr_lo, thr_hi)
                cp.pixels.fill((0, 0, 0))
                a_hold_started_at = None
                dry_stable_started_at = None
        else:
            a_hold_started_at = None

    prev_btn_a = btn_a_pressed
    prev_btn_b = btn_b_pressed

    time.sleep(0.5)
