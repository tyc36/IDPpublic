from machine import Pin
from utime import sleep
import json

with open('pin.json', 'r') as file:
    pin = json.load(file)

YELLOW_LED_PIN = pin['Yellow_LED_pin']
RED_LED_PIN= pin['Red_LED_pin']

yellow_led= Pin(YELLOW_LED_PIN, Pin.OUT)
red_led_and_sensor = Pin(RED_LED_PIN, Pin.OUT)


def yellow_led_on():
    yellow_led.value(1)     #start flasing

def yellow_led_off():
    yellow_led.value(0)     #stop flashing

def red_led_on():
    red_led_and_sensor.value(1)    # turn on the red LED when the colour sensor is powered

def red_led_off():
    red_led_and_sensor.value(0)     #turn off the red LED when colour sensor power is off
    
