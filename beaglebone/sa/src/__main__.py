import asyncio
import time
import Adafruit_BBIO.PWM as PWM
from rover_common import aiolcm
from rover_msgs import ServoCmd

SERVO_MAX_DC = 10.0
SERVO_MIN_DC = 4.0

#Blue Science Box
SERVO_BLUE_0 = "P9_14"
SERVO_BLUE_1 = "P9_16"
#Yellow Science Box
SERVO_YELLOW_0 = "P9_21"
SERVO_YELLOW_1 = "P9_22"
#White Science Box
SERVO_WHITE_0 = "P8_13"
SERVO_WHITE_1 = "P8_19"

servos = [SERVO_BLUE_0, SERVO_BLUE_1, SERVO_YELLOW_0, SERVO_YELLOW_1, SERVO_WHITE_0, SERVO_WHITE_1]

lcm_ = aiolcm.AsyncLCM()

def angle_to_dc(degrees):
    percent = degrees / 120.0
    dc = SERVO_MIN_DC + (percent * (SERVO_MAX_DC - SERVO_MIN_DC))
    return dc

def run_servo(pin, degrees):
    dc = angle_to_dc(degrees)
    PWM.set_duty_cycle(pin, dc)

def servo_init(pin, degrees):
    dc = angle_to_dc(degrees)
    PWM.start(pin, dc, 50)

def servo_callback(channel, msg):
    servo = Servo.decode(msg)
    if servo.id == "servo_1":
        run_servo(servos[0], servo.position)
    elif servo.id == "servo_2":
        run_servo(servos[1], servo.position)
    elif servo.id == "servo_3":
        run_servo(servos[2], servo.position)
    elif servo.id == "servo_4":
        run_servo(servos[3], servo.position)
    elif servo.id == "servo_5":
        run_servo(servos[4], servo.position)
    elif servo.id == "servo_6":
        run_servo(servos[5], servo.position)
    else:
        print("Invalid servo ID.")

def main():
    for pin in servos:
        servo_init(pin, 0)

    lcm_.subscribe("/servo_cmd", servo_callback)
    
