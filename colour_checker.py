import sensors

def colour_checker():
    while True:
        try:
            print("hello")
            r,g,b = sensors.get_color_value()
            if 90>r >80  and 55>g >35 and 80 >b >60:
                return 4
            if 40>r >29  and 78>g >66 and 105 >b >83:#
                return 23
            if 25>r >10  and 65>g >55 and 145 >b >112: #
                return 22
            if 69>r >50  and 95>g >75 and 79>b >35: #
                return 3
            return 22
        except OSError:
                pass
