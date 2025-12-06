from machine import Pin
from utime import sleep
import json

with open('pin.json', 'r') as file:
    pin = json.load(file)

push_button_pin = pin["push_button_pin"]

button = Pin(push_button_pin, Pin.IN, Pin.PULL_UP)

running = False
last_button_state = 0 

def update_button():
    global running, last_button_state

    current = button.value()
    sleep(0.1)

    if last_button_state == 0 and current == 1:
        running = not running
        if running:
            print("AGV STARTED")
        else:
            print("AGV STOPPED")
        sleep(0.05)  # debounce

    last_button_state = current
    print(current)
    
    return running


