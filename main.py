import motor
import sensors
import LED_control
import linear_actuator
from linefollow import line_following
from loadcontrol import loadsequence, leave_sequence, unloadsequence

import push_button
from utime import sleep
from utime import time


def AGV_control():
    linear_actuator.actuator_extend()
    linear_actuator.actuator_retract(1)
    junction_count=1
    direction = 1 #1 for clockwise 0 for anti-clockwise

    mode = "search"
    checklist_cw = []
    checklist_ccw = []
        
    while True:

        if push_button.update_button() == False:
            motor.motor_stop()
            continue

        if mode == "search":

            junction_count = line_following(junction_count, direction, mode, checklist_cw if direction ==1 else checklist_ccw)
            if direction == 1:
                d = sensors.get_TOFL_distance_avg()
                print(d)
                if d < 300 and junction_count -1 not in checklist_cw: #stuff detected
                    checklist_cw.append(junction_count -1)
                    mode = "load"
                else:
                    checklist_cw.append(junction_count -1)
                    motor.motor_forward()
                    sleep(0.2)
                    if len(checklist_cw) == 6: #prevent no box on one side where it will never get into mode load but unlikely to happen
                        motor.turn_around(direction, 2)      
                        direction = 0
                        junction_count = 28 - junction_count
                       # mode = "return"
    

                        
            else:
                d = sensors.get_TMF_distance_mm()
                print(d)
                
                if d < 700 and junction_count -1 not in checklist_ccw: #stuff detected
                    checklist_ccw.append(junction_count -1)
                    mode = "load"
                else:
                    checklist_ccw.append(junction_count -1)
                    if len(checklist_ccw) == 6:
                        motor.turn_around(direction, 2)
                        direction = 1
                        junction_count = 28 - junction_count
                      #  mode = "return"


            print(junction_count)
        elif mode == "load":
            unload_point = loadsequence(direction) # in terms of orignal direction
            mode = "unload"


        elif mode == "unload":
            leave_sequence(direction)
            direction = 1 - direction
            junction_count = 28 - junction_count  # reset junction count for return trip
            if direction == 1:
                checklist = checklist_cw
            else:
                checklist = checklist_ccw
            junction_count = line_following(junction_count, direction, mode, checklist, location=unload_point)

            direction = 1 - direction
            junction_count = 28 - junction_count
            # code to return to start


            unloadsequence(junction_count, direction)
            mode = "search"
            
            if len(checklist_cw) + len(checklist_ccw) >= 12:
                mode = "return"
                if junction_count -1 == 3 or junction_count -1 == 4: # closest return path.
                    direction = 1 - direction
                    junction_count = 28 - junction_count

        elif mode == "return":
            line_following(junction_count, direction, mode, checklist)
            LED_control.yellow_led_off()




# run

try:    
    AGV_control()
except KeyboardInterrupt:
    motor.motor_stop()
    LED_control.yellow_led_off()
    LED_control.red_led_off()
    print("Program stopped.")



