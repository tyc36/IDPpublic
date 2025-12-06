from utime import sleep
from machine import Pin, PWM


class Actuator:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)
        self.pwm = PWM(Pin(PWMPin))
        self.pwm.freq(1000)
        self.pwm.duty_u16(0)

    def set(self, dir, speed):
        self.mDir.value(dir)
        self.pwm.duty_u16(int(65535 * speed / 100))

    def stop(self):
        self.pwm.duty_u16(0)


def actuator_extend(time = 7):
    actuator = Actuator(dirPin=0, PWMPin=1)
  
    print("Extend actuator")
    actuator.set(dir=0, speed=100)
    sleep(time)
    actuator.stop()

def actuator_retract(time = 3):
    actuator = Actuator(dirPin=0, PWMPin=1)
    print("Retract actuator")
    actuator.set(dir=1, speed=100)
    sleep(time)
    actuator.stop()



