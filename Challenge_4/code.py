import time

import adafruit_irremote
import board
import pulseio
import pwmio
from adafruit_circuitplayground import cp

print("FS90R Servo Controller")

servo_pwm = pwmio.PWMOut(board.A1, frequency=50)

# Correct PWM calculations for 50Hz:
# 50Hz = 20ms period
# For 16-bit PWM (65535 max):
# 1.0ms (full reverse) = 65535 * 0.05 = 3277
# 1.5ms (stop) = 65535 * 0.075 = 4915
# 2.0ms (full forward) = 65535 * 0.1 = 6554
SERVO_STOP = 4915
SERVO_FORWARD = 6554
SERVO_REVERSE = 3277

print("Setting servo to STOP")
servo_pwm.duty_cycle = SERVO_STOP
print("Duty cycle set to:", SERVO_STOP)

ir_receiver = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
ir_decoder = adafruit_irremote.GenericDecode()


def stop_servo():
    print("Setting duty_cycle to:", SERVO_STOP)
    servo_pwm.duty_cycle = SERVO_STOP
    cp.pixels.fill((0, 0, 255))
    print("STOP")


def run_forward():
    print("Setting duty_cycle to:", SERVO_FORWARD)
    servo_pwm.duty_cycle = SERVO_FORWARD
    cp.pixels.fill((0, 255, 0))
    print("FORWARD")


def run_reverse():
    print("Setting duty_cycle to:", SERVO_REVERSE)
    servo_pwm.duty_cycle = SERVO_REVERSE
    cp.pixels.fill((255, 0, 0))
    print("REVERSE")


print("Ready")

prev_a = False
prev_b = False
prev_switch = cp.switch

while True:
    btn_a = cp.button_a
    btn_b = cp.button_b
    switch = cp.switch

    if btn_a and not prev_a:
        run_forward()

    if btn_b and not prev_b:
        run_reverse()

    if switch and not prev_switch:
        stop_servo()

    pulses = ir_decoder.read_pulses(ir_receiver, blocking=False)

    if pulses:
        if len(pulses) > 10:
            try:
                code = ir_decoder.decode_bits(pulses)
                if code and len(code) >= 2:
                    if code[0] == 255:
                        if code[1] == 1:
                            run_forward()
                        elif code[1] == 2:
                            run_reverse()
                        elif code[1] == 0:
                            stop_servo()
            except Exception:
                pass

    prev_a = btn_a
    prev_b = btn_b
    prev_switch = switch

    time.sleep(0.05)
    time.sleep(0.05)
