"""Smart actuator: voting sensor + servo-controlled pinch valve.

3-probe voting (A1, A3, A5) triggers SG92R servo (A6) to close pinch valve.
Uses minimal PWM approach for power stability with external servo power.
Non-adjacent pads reduce capacitive cross-talk between sensors.
"""

import time

import board
import pwmio
import touchio
from adafruit_circuitplayground import cp

# Initialize sensors on non-adjacent pads to reduce cross-talk
touch_pads = [
    touchio.TouchIn(board.A1),
    touchio.TouchIn(board.A3),
    touchio.TouchIn(board.A5),
]

# Servo PWM values (50Hz)
SERVO_OPEN = 3277      # 1.0ms pulse = 0°
SERVO_CLOSED = 4915    # 1.5ms pulse = 90°

# Keep PWM active for servo control
servo_pwm = pwmio.PWMOut(board.A6, frequency=50)


def move_servo(duty_cycle):
    """Move servo and hold position with continuous PWM."""
    servo_pwm.duty_cycle = duty_cycle
    time.sleep(0.5)  # Give servo time to reach position


# Initialize servo to open position
move_servo(SERVO_OPEN)
print("Servo initialized to OPEN position")
print("Baselines will be captured in 2 seconds...")

# Simplified settings
PIXEL_COUNT = 10
cp.pixels.brightness = 0.2
cp.pixels.fill((0, 0, 0))

# Auto-calibration (simplified - fewer samples)


def capture_baseline(pad):
    readings = []
    for _ in range(20):  # reduced from 40
        readings.append(pad.raw_value)
        time.sleep(0.05)
    readings.sort()
    return readings[10]


cp.pixels[0] = (255, 140, 0)
dry_baselines = [capture_baseline(p) for p in touch_pads]
cp.pixels[0] = (0, 0, 0)
print(
    f"Baselines: A1={dry_baselines[0]}, "
    f"A3={dry_baselines[1]}, A5={dry_baselines[2]}")

# Load margin
threshold_margin = 1000
try:
    with open("cal.txt", "r") as f:
        threshold_margin = int(f.read().strip())
except (OSError, ValueError):
    pass

thr_lo = [b - threshold_margin for b in dry_baselines]
thr_hi = [b + threshold_margin for b in dry_baselines]

print(f"Threshold margin: {threshold_margin}")
print("=== System Ready ===")
print("Touch 2+ probes to close valve (red LED on)")
print("Remove probes to open valve (red LED off)")
print("Button A: decrease sensitivity | Button B: increase sensitivity")
print()

# Servo already initialized to OPEN and deinitialized above

# State
wet_counts = [0, 0, 0]
dry_counts = [0, 0, 0]
probe_wet = [False, False, False]
majority_wet = False
prev_majority_wet = False

prev_btn_a = False
prev_btn_b = False
MARGIN_STEP = 100

# Auto-tracking state
tracking_enabled = True
TRACKING_RATE = 0.02  # 2% adjustment per update
TRACKING_INTERVAL = 50  # Update every 50 loops (~5 sec)
loop_count = 0


while True:
    raw_values = [p.raw_value for p in touch_pads]

    # Per-probe hysteresis
    for i in range(3):
        if (raw_values[i] > thr_hi[i]) or (raw_values[i] < thr_lo[i]):
            wet_counts[i] = min(wet_counts[i] + 1, 3)
            dry_counts[i] = 0
        else:
            dry_counts[i] = min(dry_counts[i] + 1, 3)
            wet_counts[i] = 0
        probe_wet[i] = wet_counts[i] >= 2

    # Majority vote
    majority_wet = (probe_wet.count(True) >= 2)

    # Auto-tracking: slowly adjust baselines when all probes agree (dry)
    if tracking_enabled and not majority_wet:
        loop_count += 1
        if loop_count >= TRACKING_INTERVAL:
            loop_count = 0
            if probe_wet.count(False) == 3:  # All dry
                for i in range(3):
                    diff = raw_values[i] - dry_baselines[i]
                    adjustment = int(diff * TRACKING_RATE)
                    if abs(adjustment) > 0:
                        dry_baselines[i] += adjustment
                        thr_lo[i] = dry_baselines[i] - threshold_margin
                        thr_hi[i] = dry_baselines[i] + threshold_margin

    # Control servo (only when state changes - minimal PWM pulses)
    if majority_wet and not prev_majority_wet:
        print("MAJORITY WET -> Closing valve")
        move_servo(SERVO_CLOSED)
        cp.red_led = True
    elif not majority_wet and prev_majority_wet:
        print("MAJORITY DRY -> Opening valve")
        move_servo(SERVO_OPEN)
        cp.red_led = False
    prev_majority_wet = majority_wet

    # Simple visualization - light pixel count based on wet probes
    wet_count_total = probe_wet.count(True)
    for i in range(PIXEL_COUNT):
        if i < wet_count_total * 3:
            cp.pixels[i] = (100, 50, 0)
        else:
            cp.pixels[i] = (0, 0, 0)

    # Detailed LED bar graph - show individual probe status
    # Probes: A1=pixels 0-2, A2=pixels 3-5, A3=pixels 6-8, pixel 9=majority
    for i in range(3):
        color = (0, 100, 100) if probe_wet[i] else (0, 20, 0)
        for j in range(3):
            cp.pixels[i * 3 + j] = color
    # Pixel 9 shows majority vote status
    cp.pixels[9] = (255, 0, 0) if majority_wet else (0, 50, 0)

    # Button tuning
    btn_a = cp.button_a
    btn_b = cp.button_b

    if btn_a and not prev_btn_a:
        threshold_margin = max(0, threshold_margin - MARGIN_STEP)
        thr_lo = [b - threshold_margin for b in dry_baselines]
        thr_hi = [b + threshold_margin for b in dry_baselines]
        print(f"Margin decreased to {threshold_margin}")
    if btn_b and not prev_btn_b:
        threshold_margin = min(8000, threshold_margin + MARGIN_STEP)
        thr_lo = [b - threshold_margin for b in dry_baselines]
        thr_hi = [b + threshold_margin for b in dry_baselines]
        print(f"Margin increased to {threshold_margin}")

    prev_btn_a = btn_a
    prev_btn_b = btn_b

    time.sleep(0.1)
