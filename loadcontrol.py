import motor
from sensors import line_sensors
import colour_checker
import linear_actuator
import push_button
from utime import sleep

def loadsequence(direction):
    if direction == 1:  # clockwise
        motor.motor_right_turn()
        linear_actuator.actuator_retract()
        while True:
            if push_button.update_button() == False:
                motor.motor_stop()
                continue
            sleep(0.03)
            side , mid = line_sensors()
            L, R = side
            ML , MR = mid
            if mid == (1,1):
                motor.motor_forward()

            elif mid == (0,0):
                motor.motor_stop()
             #  print("stopped")
                location = colour_checker.colour_checker()
                linear_actuator.actuator_retract(time = 2)
                return location
            else:
                # proportional control
                error = (-1 * ML) + (1 * MR)
                correction = 15 * error

                left_speed = 50 + correction
                right_speed = 50 - correction

                motor.motor_forward(left_speed, right_speed)
               # print(f"{L, ML, MR, R} | Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")
            

    else:  # anti-clockwise
        sleep(0.3)
        motor.motor_left_turn()
        linear_actuator.actuator_retract()
        while True:
            if push_button.update_button() == False:
                motor.motor_stop()
                continue
            sleep(0.03)
            side , mid = line_sensors()
            L, R = side
            ML , MR = mid
            if mid == (1,1):
                motor.motor_forward()

            elif mid == (0,0):
                motor.motor_stop()
                location = 26 - colour_checker.colour_checker()
                linear_actuator.actuator_retract(time = 2)
                return location
            else:
                # proportional control
                error = (-1 * ML) + (1 * MR)
                correction = 15 * error

                left_speed = 50 + correction
                right_speed = 50 - correction

                motor.motor_forward(left_speed, right_speed)
            #    print(f"{L, ML, MR, R} | Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")

def leave_sequence(direction):
    if direction == 1:  # clockwise
        motor.motor_backward()
        sleep(0.8)
        motor.motor_stop()
        linear_actuator.actuator_extend(3)
        motor.motor_backward()
        sleep(0.5)
        motor.motor_right_turn()
        
        return True

    else:  # anti-clockwise 
        motor.motor_backward()
        sleep(0.8)
        motor.motor_stop()
        linear_actuator.actuator_extend(3)
        motor.motor_backward()
        sleep(0.5)
        motor.motor_left_turn()

        return True
    
def unloadsequence(junction_count, direction):
    linear_actuator.actuator_extend(7)
    motor.motor_backward()
    sleep(0.5)
    if (direction == 1 and junction_count == 23) or (direction == 0 and junction_count == 5):
        motor.turn_around(1)
    else:
        motor.turn_around(0)
    linear_actuator.actuator_retract(1)
    while True:
        if push_button.update_button() == False:
            motor.motor_stop()
            continue
        sleep(0.03)
        side , mid = line_sensors()
        L, R = side
        ML , MR = mid
        if direction == 0:
            if junction_count -1 == 22 and side == (0,1):
                sleep(0.1)
                motor.normal_right_turn()
                return
            elif junction_count -1 == 23 and side == (1,1):
                sleep(0.1)
                motor.normal_right_turn()
                return
            elif junction_count -1 == 3 and side == (1,1):
                sleep(0.1)
                motor.normal_right_turn()
                return
            elif junction_count -1 == 4 and side == (1,0):
                motor.motor_forward()
                return
        elif direction == 1:
            if junction_count -1== 4 and side == (0,1):
                motor.motor_forward()
                return
            elif junction_count -1 == 3 and side == (1,1):
                sleep(0.1)
                motor.normal_left_turn()
                return
            elif junction_count -1 == 23 and side == (1,1):
                sleep(0.1)
                motor.normal_left_turn()
                return
            elif junction_count -1 == 22 and side == (1,0):
                sleep(0.1)
                motor.normal_left_turn()
                return
        
        if mid == (1,1):
            motor.motor_forward()
        else:
            # proportional control
            error = (-1 * ML) + (1 * MR)
            correction = 30 * error

            left_speed = 60 + correction
            right_speed = 60 - correction

            motor.motor_forward(left_speed, right_speed)
            sleep(0.1)
            motor.motor_forward()
           # print(f"{L, ML, MR, R} | Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")




