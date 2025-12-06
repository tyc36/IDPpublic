import sensors
import json
from map_reader import MapReader
from utime import sleep

map_reader = MapReader()

def check_junction(junction_count, direction):
    side, mid = sensors.line_sensors()


    pattern = map_reader.get_pattern(junction_count, direction)

    if side == pattern:
        actions = map_reader.get_actions(junction_count, direction)
        junction_count+=1
        return actions, side, mid, junction_count
    else:
        return "normal", side, mid, junction_count





