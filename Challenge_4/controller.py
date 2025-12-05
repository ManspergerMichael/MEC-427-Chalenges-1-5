"""Motor Controller - CPX Remote Control

This CPX acts as a wireless remote using infrared communication.

Controls:
- Button A: Send "forward" command
- Button B: Send "reverse" command  
- Slide Switch Left: Send "stop" command
- Slide Switch Right: Enable control

LED Indicators:
- Blue: Ready
- Green: Command sent successfully
- Yellow: Transmitting
"""

import time

import adafruit_irremote
import board
import pulseio
from adafruit_circuitplayground import cp

print("=== Motor Remote Control ===")
print("Button A: Forward")
print("Button B: Reverse")
print("Switch Left: Stop")
print()

# IR transmitter setup (uses pin A1)
ir_transmitter = pulseio.PulseOut(
    board.IR_TX, frequency=38000, duty_cycle=2 ** 15)
ir_encoder = adafruit_irremote.GenericTransmit(
    header=[9500, 4500], one=[560, 1680], zero=[560, 560], trail=560)

# Command codes
CMD_FORWARD = [255, 1]   # Forward command
CMD_REVERSE = [255, 2]   # Reverse command
CMD_STOP = [255, 0]      # Stop command

# LED setup
cp.pixels.brightness = 0.2
cp.pixels.fill((0, 0, 255))  # Blue = ready


def send_command(cmd, name):
    """Send IR command and provide feedback."""
    print(f"Sending: {name}")
    cp.pixels.fill((255, 255, 0))  # Yellow while transmitting

    # Send command 3 times for reliability
    for i in range(3):
        ir_encoder.transmit(ir_transmitter, cmd)
        time.sleep(0.05)

    cp.pixels.fill((0, 255, 0))  # Green = sent
    time.sleep(0.2)
    cp.pixels.fill((0, 0, 255))  # Back to blue


prev_a = False
prev_b = False
prev_switch = cp.switch

print("Ready to send commands\n")

while True:
    btn_a = cp.button_a
    btn_b = cp.button_b
    switch = cp.switch

    # Button A: Forward
    if btn_a and not prev_a:
        send_command(CMD_FORWARD, "FORWARD")

    # Button B: Reverse
    if btn_b and not prev_b:
        send_command(CMD_REVERSE, "REVERSE")

    # Switch changed to left: Stop
    if switch and not prev_switch:
        send_command(CMD_STOP, "STOP")

    prev_a = btn_a
    prev_b = btn_b
    prev_switch = switch

    time.sleep(0.05)
    time.sleep(0.05)
