"""Motor Receiver - CPX Motor Controller

This CPX receives IR commands OR local button presses to control the N20 motor.

DRV8833 Wiring:
- CPX A1 -> DRV8833 IN1 (PWM forward)
- CPX A2 -> DRV8833 IN2 (PWM reverse)
- CPX A6 -> DRV8833 FLT (fault detection)
- CPX GND -> DRV8833 GND
- Battery + (7.4V) -> DRV8833 VCC (combined logic/motor power)
- Battery - -> DRV8833 GND (common with CPX)
- Motor -> DRV8833 OUT1 and OUT2
- SLEEP -> VCC (jumper)

Controls:
- Button A (local or IR): Run forward
- Button B (local or IR): Run reverse
- Switch Left (local or IR): Stop

LED Indicators:
- Blue: Idle/stopped
- Green: Running forward
- Red: Running reverse
- Yellow: Fault detected
"""

import time

import adafruit_irremote
import board
import digitalio
import pulseio
import pwmio
from adafruit_circuitplayground import cp

print("=== Motor Controller ===")
print("Local Controls:")
print("  Button A: Forward")
print("  Button B: Reverse")
print("  Switch Left: Stop")
print("Also listening for IR commands...")
print()

# Motor control pins
in1_pin = pwmio.PWMOut(board.A1, frequency=1000)
in2_pin = pwmio.PWMOut(board.A2, frequency=1000)

# Fault detection pin
flt_pin = digitalio.DigitalInOut(board.A6)
flt_pin.direction = digitalio.Direction.INPUT
flt_pin.pull = digitalio.Pull.UP

# IR receiver setup
ir_receiver = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
ir_decoder = adafruit_irremote.GenericDecode()

# Motor stopped initially
in1_pin.duty_cycle = 0
in2_pin.duty_cycle = 0

# LED setup
cp.pixels.brightness = 0.2
cp.pixels.fill((0, 0, 255))  # Blue = idle

# Command codes (must match controller)
CMD_FORWARD = [255, 1]
CMD_REVERSE = [255, 2]
CMD_STOP = [255, 0]

motor_state = "stopped"


def check_fault():
    """Check for fault and stop motor if detected."""
    if not flt_pin.value:
        print("⚠️  FAULT!")
        stop_motor()
        cp.pixels.fill((255, 255, 0))  # Yellow
        return True
    return False


def stop_motor():
    """Stop the motor."""
    global motor_state
    in1_pin.duty_cycle = 0
    in2_pin.duty_cycle = 0
    motor_state = "stopped"
    cp.pixels.fill((0, 0, 255))  # Blue
    print("Motor: STOP")


def run_forward():
    """Run motor forward at 100%."""
    global motor_state
    if check_fault():
        return
    in1_pin.duty_cycle = 65535
    in2_pin.duty_cycle = 0
    motor_state = "forward"
    cp.pixels.fill((0, 255, 0))  # Green
    print("Motor: FORWARD 100%")


def run_reverse():
    """Run motor reverse at 100%."""
    global motor_state
    if check_fault():
        return
    in1_pin.duty_cycle = 0
    in2_pin.duty_cycle = 65535
    motor_state = "reverse"
    cp.pixels.fill((255, 0, 0))  # Red
    print("Motor: REVERSE 100%")


# Check initial fault status
if not flt_pin.value:
    print("⚠️  FAULT at startup!")
    cp.pixels.fill((255, 255, 0))
else:
    print("✓ Ready to receive commands")

print()

# Main loop
prev_a = False
prev_b = False
prev_switch = cp.switch

print("Ready - try pressing Button A\n")

while True:
    btn_a = cp.button_a
    btn_b = cp.button_b
    switch = cp.switch

    # Local button controls
    if btn_a and not prev_a:
        print("Button A pressed!")
        run_forward()

    if btn_b and not prev_b:
        print("Button B pressed!")
        run_reverse()

    if switch and not prev_switch:
        print("Switch moved to left!")
        stop_motor()

    # Check for IR messages (non-blocking)
    pulses = ir_decoder.read_pulses(ir_receiver, blocking=False)

    if pulses:
        try:
            code = ir_decoder.decode_bits(pulses)
            if code:
                print(f"IR received: {code}")
                # Process IR command
                if code == CMD_FORWARD:
                    run_forward()
                elif code == CMD_REVERSE:
                    run_reverse()
                elif code == CMD_STOP:
                    stop_motor()
        except Exception as e:
            pass  # Ignore decode errors

    # Periodic fault check
    if motor_state != "stopped":
        check_fault()

    prev_a = btn_a
    prev_b = btn_b
    prev_switch = switch

    time.sleep(0.05)
    pass  # Ignore decode errors

    # Periodic fault check
    if motor_state != "stopped":
        check_fault()

    prev_a = btn_a
    prev_b = btn_b
    prev_switch = switch

    time.sleep(0.01)
