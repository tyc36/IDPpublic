from sensors import line_sensors

class LineCounter:
    def __init__(self, threshold=2):
        self.threshold = threshold
        self.count = 0
        self.last_was_on_line = None  # assume we dont know initial state putting to True works the same

    def update(self):
        _, mid = line_sensors()  # ignore left/right
        on_line = mid == (1,1)

        if on_line and self.last_was_on_line == False:
            self.count += 1

        self.last_was_on_line = on_line

        return self.count == self.threshold
