"""N20 DC Motor Testing Suite for Circuit Playground Express

DRV8833 Wiring:
- CPX A1 -> DRV8833 AIN1 (PWM speed)
- CPX A2 -> DRV8833 AIN2 (direction)
- CPX GND -> DRV8833 GND
- Motor + -> DRV8833 AO1
- Motor - -> DRV8833 AO2
- Battery + -> DRV8833 VCC
- Battery - -> DRV8833 GND (same as CPX GND)

Button A: Run test sequence
Button B: Emergency stop
"""

import time

import board
import digitalio
import pwmio
from adafruit_circuitplayground import cp

print("=== N20 Motor Test Suite ===")
print("Wiring Check:")
print(f"  A1 (AIN1/PWM) -> DRV8833 AIN1")
print(f"  A2 (AIN2/DIR) -> DRV8833 AIN2")
print("Button A: Run test sequence")
print("Button B: Emergency stop")
print()

# Motor control pins
pwm_pin = pwmio.PWMOut(board.A1, frequency=1000)
dir_pin = digitalio.DigitalInOut(board.A2)
dir_pin.direction = digitalio.Direction.OUTPUT

# Motor stopped initially
pwm_pin.duty_cycle = 0
dir_pin.value = False

# LED setup
cp.pixels.brightness = 0.2
cp.pixels.fill((0, 0, 255))  # Blue = ready

test_running = False


def stop_motor():
    """Immediately stop the motor."""
    pwm_pin.duty_cycle = 0
    print("Motor stopped")


def set_motor(speed, direction):
    """Set motor speed and direction.

    speed: 0-100 (percentage)
    direction: True=forward, False=reverse
    """
    dir_pin.value = direction
    duty = int((speed / 100.0) * 65535)
    pwm_pin.duty_cycle = duty
    dir_str = "FWD" if direction else "REV"
    print(f"Motor: {speed}% {dir_str} | AIN1(PWM)={duty} AIN2(DIR)={direction}")


def test_sequence():
    """Run complete motor test sequence."""
    global test_running
    test_running = True

    print("\n=== Starting Test Sequence ===")
    cp.pixels.fill((255, 255, 0))  # Yellow = testing

    # Test 1: Gradual speed ramp forward
    print("\nTest 1: Forward ramp (0-100%)")
    for speed in range(0, 101, 20):
        if not test_running:
            return
        set_motor(speed, True)
        time.sleep(1)
    stop_motor()
    time.sleep(1)

    # Test 2: Gradual speed ramp reverse
    print("\nTest 2: Reverse ramp (0-100%)")
    for speed in range(0, 101, 20):
        if not test_running:
            return
        set_motor(speed, False)
        time.sleep(1)
    stop_motor()
    time.sleep(1)

    # Test 3: Quick direction changes at 50%
    print("\nTest 3: Direction changes (50% speed)")
    for i in range(4):
        if not test_running:
            return
        set_motor(50, True)
        time.sleep(1)
        if not test_running:
            return
        set_motor(50, False)
        time.sleep(1)
    stop_motor()
    time.sleep(1)

    # Test 4: PWM frequency test (constant 50% speed)
    print("\nTest 4: Different speeds forward")
    speeds = [25, 50, 75, 100, 75, 50, 25]
    for speed in speeds:
        if not test_running:
            return
        set_motor(speed, True)
        time.sleep(1.5)
    stop_motor()

    print("\n=== Test Complete ===")
    cp.pixels.fill((0, 255, 0))  # Green = success
    time.sleep(2)
    cp.pixels.fill((0, 0, 255))  # Back to blue
    test_running = False


prev_btn_a = False
prev_btn_b = False

while True:
    btn_a = cp.button_a
    btn_b = cp.button_b

    # Button A: Start test sequence
    if btn_a and not prev_btn_a and not test_running:
        test_sequence()

    # Button B: Emergency stop
    if btn_b and not prev_btn_b:
        test_running = False
        stop_motor()
        cp.pixels.fill((255, 0, 0))  # Red = stopped
        print("\n!!! EMERGENCY STOP !!!")
        time.sleep(1)
        cp.pixels.fill((0, 0, 255))  # Back to blue

    prev_btn_a = btn_a
    prev_btn_b = btn_b

    time.sleep(0.1)
    time.sleep(0.1)
