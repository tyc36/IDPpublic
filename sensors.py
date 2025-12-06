from machine import Pin, PWM, ADC, I2C
from utime import sleep
import json
import LED_control
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.tcs3472_micropython.tcs3472 import tcs3472
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701

with open('pin.json', 'r') as file:
    pin = json.load(file)

line_sensor_left_pin = pin['line_sensor_left_pin']
line_sensor_midL_pin = pin['line_sensor_midL_pin']
line_sensor_midR_pin = pin['line_sensor_midR_pin']
line_sensor_right_pin = pin['line_sensor_right_pin']

ultrasonic_sensor_pin = pin['ultrasonic_sensor_pin']

color_sensor_SDA_pin = pin['color_sensor_SDA_pin']  #I2C0 for color_sensor
color_sensor_SCL_pin = pin['color_sensor_SCL_pin']

TMFR_SDA_pin = pin['TMFR_SDA_pin']
TMFR_SCL_pin = pin['TMFR_SCL_pin']
TOFL_SDA_pin = TMFR_SDA_pin         #share I2C1
TOFL_SCL_pin = TMFR_SCL_pin


#---------------------line sensors-------------------------------------
line_sensor_left = Pin(line_sensor_left_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_midL = Pin(line_sensor_midL_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_midR = Pin(line_sensor_midR_pin, Pin.IN, Pin.PULL_DOWN)
line_sensor_right = Pin(line_sensor_right_pin, Pin.IN, Pin.PULL_DOWN)
#Read line sensor states
def line_sensors():
    left_state = line_sensor_left.value()
    right_state = line_sensor_right.value()

    midL_state = line_sensor_midL.value()
    midR_state = line_sensor_midR.value()
    return (left_state, right_state), (midL_state, midR_state)

# -------------------- COLOR SENSOR (TCS3472)-----------------------------
# i2c0 = I2C(1, sda=Pin(color_sensor_SDA_pin), scl=Pin(color_sensor_SCL_pin), freq=100000)


# def color_sensor_reading(tcs, samples=1000):
#     values = []
#     for i in range(samples):
#         values.append(tcs.light())
#     values.sort()
#     cut = samples // 10    # remove top and bottom 10% noise
#     trimmed = values[cut : samples - cut]
#     return sum(trimmed) / len(trimmed)


# def get_color_value(samples=100):   #call this when need to read color
#     LED_control.red_led_on()  
#     tcs = tcs3472(i2c0)
#     sleep(0.5)# initialize 
#     value = color_sensor_reading(tcs, samples)
#     LED_control.red_led_off()
#     sleep(7)
#     return value

# -------------------- COLOR SENSOR (TCS3472) -----------------------------
i2c0 = I2C(1, sda=Pin(color_sensor_SDA_pin), scl=Pin(color_sensor_SCL_pin), freq=100000)



def read_normalized_rgb(tcs):
    return  tcs.rgb()



def get_color_value(samples=200):
    LED_control.red_led_on()
    sleep(0.2)

    tcs = tcs3472(i2c0)

    rs, gs, bs = [], [], []

    for _ in range(samples):
        r, g, b = read_normalized_rgb(tcs)
        rs.append(r); gs.append(g); bs.append(b)
        sleep(0.01)

    LED_control.red_led_off()

    r_avg = sum(rs) / len(rs)
    g_avg = sum(gs) / len(gs)
    b_avg = sum(bs) / len(bs)

    return r_avg, g_avg, b_avg







# ----------------------TMF8701 + VL53L0X----------------------------------
i2c1 = I2C(0,sda=Pin(TMFR_SDA_pin), scl=Pin(TMFR_SCL_pin),freq=100000)

# VL53L0X TOF
tof_left = VL53L0X(i2c1)
tof_left.set_Vcsel_pulse_period(tof_left.vcsel_period_type[0], 18)
tof_left.set_Vcsel_pulse_period(tof_left.vcsel_period_type[1], 14)
tof_left.start()

def get_TOFL_distance():
    return tof_left.read()

def get_TOFL_distance_avg(samples=20):
    total = 0

    for _ in range(samples):
        total += tof_left.read()

    return total / samples



# TMF8701 (shorter-range)
tmf = DFRobot_TMF8701(i2c_bus=i2c1)
tmf.begin()
tmf.start_measurement(calib_m=tmf.eMODE_NO_CALIB, mode=tmf.eCOMBINE)

def get_TMF_distance_mm():
    if tmf.is_data_ready():
        return tmf.get_distance_mm()

def get_TMF_distance_mm_avg(samples=20):
    total = 0
    count = 0

    for i in range(samples):

        # keep trying until we dont get none
        while True:
            if tmf.is_data_ready():
                d = tmf.get_distance_mm()
                if d is not None and d > 0:
                    break

        total += d
        count += 1

    return total / count



#while True:
   # print(get_color_value())
#     LED_control.red_led_on()
#     sleep(0.05)   
#     tcs = tcs3472(i2c0)
#     reading = color_sensor_reading(tcs)
#     print("color:", reading)
#     LED_control.red_led_off()
#     print("off")
#     sleep(1)

