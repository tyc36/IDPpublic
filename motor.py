from machine import Pin, PWM
from utime import sleep
from linecounter import LineCounter
import sensors
import json

with open('pin.json', 'r') as file:
    pin = json.load(file)

#pins from pin.json
motor_left_pin = pin['motor_left_pin']
motor_left_pwm = pin['motor_left_pwm']
motor_right_pin = pin['motor_right_pin']
motor_right_pwm = pin['motor_right_pwm']

#setup motor pins
motor_left = Pin(motor_left_pin, Pin.OUT)
motor_pwn_left = PWM(Pin(motor_left_pwm))
motor_right = Pin(motor_right_pin, Pin.OUT)
motor_pwn_right = PWM(Pin(motor_right_pwm))


motor_pwn_left.freq(3000)
motor_pwn_right.freq(3000)


#Duty cycle conversion
def duty_to_u16(duty):
    """Convert duty cycle (0–100%) to 16-bit value."""
    return int((duty * 65536) / 100)

#Motor controls
#Default speed = 100
def motor_forward(left_speed = 70, right_speed = 70):
    left_duty = duty_to_u16(left_speed)
    right_duty = duty_to_u16(right_speed)

    motor_left.value(0) 
    motor_pwn_left.duty_u16(left_duty)
    motor_right.value(1)  
    motor_pwn_right.duty_u16(right_duty)

def motor_backward(left_speed = 100, right_speed = 98):
    left_duty = duty_to_u16(left_speed)
    right_duty = duty_to_u16(right_speed)

    motor_left.value(1) 
    motor_pwn_left.duty_u16(left_duty)
    motor_right.value(0)  
    motor_pwn_right.duty_u16(right_duty)

def motor_left_turn(threshold = 1, left_speed = 100, right_speed = 100):
    line_counter = LineCounter(threshold=threshold)
        
    left_duty = duty_to_u16(left_speed)
    right_duty = duty_to_u16(right_speed)

    motor_left.value(1) 
    motor_pwn_left.duty_u16(left_duty)
    motor_right.value(1)  
    motor_pwn_right.duty_u16(right_duty)
    sleep(0.2) # tehnically we dont need this but leave for now
    while True:
        if line_counter.update():
            sleep(0.1)
            motor_stop()
            break


def motor_right_turn(threshold = 1, left_speed = 100, right_speed = 100):
    line_counter = LineCounter(threshold=threshold)
    
    left_duty = duty_to_u16(left_speed)
    right_duty = duty_to_u16(right_speed)

    motor_left.value(0) 
    motor_pwn_left.duty_u16(left_duty)
    motor_right.value(0)  
    motor_pwn_right.duty_u16(right_duty)
    sleep(0.2)
    while True:
        if line_counter.update():
            sleep(0.1)
            motor_stop()
            break

def normal_left_turn(threshold = 1, left_speed = 30, right_speed = 100):
    line_counter = LineCounter(threshold=threshold)

    left_duty = duty_to_u16(left_speed)
    right_duty = duty_to_u16(right_speed)

    motor_left.value(1) 
    motor_pwn_left.duty_u16(left_duty)
    motor_right.value(1)  
    motor_pwn_right.duty_u16(right_duty)
    sleep(0.2)
    while True:
        if line_counter.update():
            sleep(0.1)
            motor_stop()
            break

def normal_right_turn(threshold = 1, left_speed = 100, right_speed = 40):
    line_counter = LineCounter(threshold=threshold)

    left_duty = duty_to_u16(left_speed)
    right_duty = duty_to_u16(right_speed)

    motor_left.value(0) 
    motor_pwn_left.duty_u16(left_duty)
    motor_right.value(0)  
    motor_pwn_right.duty_u16(right_duty)
    sleep(0.2)
    while True:
        if line_counter.update():
            sleep(0.1)
            motor_stop()
            break


def turn_around(direction, threshold = 1, left_speed = 50, right_speed = 50):
    line_counter = LineCounter(threshold=threshold)

    if direction == 1:  # clockwise
        motor_left.value(0) 
        motor_pwn_left.duty_u16(duty_to_u16(left_speed))
        motor_right.value(0)  
        motor_pwn_right.duty_u16(duty_to_u16(right_speed))
    else:  # anti-clockwise
        motor_left.value(1) 
        motor_pwn_left.duty_u16(duty_to_u16(left_speed))
        motor_right.value(1)  
        motor_pwn_right.duty_u16(duty_to_u16(right_speed))
    sleep(0.2)
    while True:
        if line_counter.update():
            sleep(0.1)
            motor_stop()
            break
        
    return



def motor_stop():
    motor_pwn_left.duty_u16(0)
    motor_pwn_right.duty_u16(0)
    motor_left.value(0)
    motor_right.value(0)
    







