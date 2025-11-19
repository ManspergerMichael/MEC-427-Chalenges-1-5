"""Ultra-minimal servo test - absolute minimum power approach.

Delays init, no servo library overhead, raw PWM only.
"""

import time

import board
import pwmio
from adafruit_circuitplayground import cp

print("=== Minimal PWM Servo Test ===")
print("Press A for single pulse test")
print()

cp.pixels.brightness = 0.05  # Reduce LED power draw
cp.pixels.fill((0, 0, 255))
time.sleep(1)
cp.pixels.fill((0, 0, 0))  # Turn off LEDs to save power

print("Ready - PWM not initialized yet")

# Servo PWM values (50Hz = 20ms period = 65535 max duty)
# 1.5ms = neutral (90°) = ~4915 duty_cycle
# 1.0ms = 0° = ~3277 duty_cycle
# 2.0ms = 180° = ~6553 duty_cycle


def send_pulse(duty, duration_ms):
    """Send a single PWM pulse then disable."""
    pwm = pwmio.PWMOut(board.A6, frequency=50)
    pwm.duty_cycle = duty
    time.sleep(duration_ms / 1000.0)
    pwm.deinit()
    print(f"  Pulse sent: duty={duty}, disabled")


test_count = 0

while True:
    if cp.button_a:
        test_count += 1
        print(f"\n--- Test {test_count}: Minimal Pulse ---")

        print("Sending 0° pulse (200ms only)...")
        send_pulse(3277, 200)
        time.sleep(1)

        print("Sending 90° pulse (200ms only)...")
        send_pulse(4915, 200)
        time.sleep(1)

        print("Test complete!")

        while cp.button_a:
            time.sleep(0.1)

    time.sleep(0.1)
    time.sleep(0.1)
