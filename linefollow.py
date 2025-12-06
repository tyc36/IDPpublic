import motor
import sensors
import LED_control
from junction_checker import check_junction
import push_button
from utime import sleep
from utime import time
from utime import ticks_ms, ticks_diff


def line_following(junction_count, direction, mode, checklist, location=None, Kp=30,base_speed=60):
 #   print("normal line following...")

    while mode == "search":
        if push_button.update_button() == False:
           motor.motor_stop()
           continue 
        
        actions, side_sensor_reading, mid_sensor_reading, junction_count = check_junction(junction_count, direction)

        if junction_count == 2 or junction_count == 3:
            LED_control.yellow_led_on()
      
        #L, R = side_sensor_reading
        ML , MR = mid_sensor_reading
        if junction_count -1 in (5,6,7,8,9,10) and junction_count - 1 not in checklist: # and if mode == "search" removed
            print(junction_count -1 not in checklist)
            print(junction_count)
            print(checklist)
            sleep(0.4)
            motor.motor_stop()
            return junction_count
        
        elif actions[0] == "forward":
            motor.motor_forward()
            sleep(0.3)

        elif actions[0] == "turn_left":
            sleep(0.1)
            motor.normal_left_turn()

        elif actions[0] == "turn_right":
            sleep(0.2)
            motor.normal_right_turn()

        elif mid_sensor_reading == (1,1):
            # on line
            motor.motor_forward()
          #  print("On line:", mid_sensor_reading)

        else:
            # proportional control
            error = (-1 * ML) + (1 * MR)
            correction = Kp * error

            left_speed = base_speed + correction
            right_speed = base_speed - correction

            motor.motor_forward(left_speed, right_speed)
            print(f"{ML, MR}| Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")
    
    
    while mode == "unload":
        if push_button.update_button() == False:
           motor.motor_stop()
           continue 
        
        actions, side_sensor_reading, mid_sensor_reading, junction_count = check_junction(junction_count, direction)
        
        print(junction_count)
        
        if junction_count == location + 1:
            print("Reached location")
          #  print(f"{junction_count}2222222222")
            while True:
                if push_button.update_button() == False:
                    motor.motor_stop()
                    continue
                _, side_sensor_reading, mid_sensor_reading, _ = check_junction(junction_count, direction)
                L, R = side_sensor_reading
                ML , MR = mid_sensor_reading
            #    print(f"{junction_count}2222222222")

                if actions[1] == "forward":
                    motor.motor_forward()
                    sleep(0.2)

                elif actions[1] == "turn_left":
                    sleep(0.3)
                    motor.normal_left_turn()

                elif actions[1] == "turn_right":
                    sleep(0.3)
                    motor.normal_right_turn()

                elif mid_sensor_reading == (1,1):
                    # on line
                    motor.motor_forward()
                    print("On line:", mid_sensor_reading)

                else:
                    # proportional control
                    error = (-1 * ML) + (1 * MR)
                    correction = Kp * error

                    left_speed = base_speed + correction
                    right_speed = base_speed - correction

                    motor.motor_forward(left_speed, right_speed)
                    print(f"{L, ML, MR, R} | Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")
                
                if side_sensor_reading == (1,1):
                    motor.motor_stop()
                    return junction_count

        # print spam prevention

        if junction_count == 25:
            junction_count = 3


        L, R = side_sensor_reading
        ML , MR = mid_sensor_reading



        if actions[0] == "forward":
            motor.motor_forward()
            sleep(0.3)

        elif actions[0] == "turn_left":
            sleep(0.1)
            motor.normal_left_turn()

        elif actions[0] == "turn_right":
            sleep(0.2)
            motor.normal_right_turn()

        elif mid_sensor_reading == (1,1):
            # on line
            motor.motor_forward()
         #   print("On line:", mid_sensor_reading)

        else:
            # proportional control
            error = (-1 * ML) + (1 * MR)
            correction = Kp * error

            left_speed = base_speed + correction
            right_speed = base_speed - correction

            motor.motor_forward(left_speed, right_speed)
            sleep(0.1)
            motor.motor_forward()
            print(f"{L, ML, MR, R} | Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")
    
    while mode == "return":
        if push_button.update_button() == False:
           motor.motor_stop()
           continue 
        #sleep(0.01)

        actions, side_sensor_reading, mid_sensor_reading, junction_count = check_junction(junction_count, direction)
        
        L, R = side_sensor_reading
        ML , MR = mid_sensor_reading

        if junction_count == 26:
            if actions[1] == "turn_left":
                sleep(0.3)
                motor.motor_left_turn()
            elif actions[1] == "turn_right":
                sleep(0.3)
                motor.motor_right_turn()
            motor.motor_forward()
            sleep(2)
            motor.motor_stop()
            return

        if actions[0] == "forward":
            motor.motor_forward()
            sleep(0.3)

        elif actions[0] == "turn_left":
            sleep(0.1)
            motor.normal_left_turn()

        elif actions[0] == "turn_right":
            sleep(0.2)
            motor.normal_right_turn()

        elif mid_sensor_reading == (1,1):
            # on line
            motor.motor_forward()
        #    print("On line:", mid_sensor_reading)

        else:
            # proportional control
            error = (-1 * ML) + (1 * MR)
            correction = Kp * error

            left_speed = base_speed + correction
            right_speed = base_speed - correction

            motor.motor_forward(left_speed, right_speed)
            print(f"{L, ML, MR, R} | Err:{error} | LS:{left_speed:.1f} RS:{right_speed:.1f}")
        

