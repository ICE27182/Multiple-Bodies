

import math
from shutil import get_terminal_size
try:
    import msvcrt
    key_capture = True
except ModuleNotFoundError:
    key_capture = False




class Body:
    palette = {
                "Black": "\033[30m",
                "Red": "\033[31m",
                "Green": "\033[32m",
                "Yellow": "\033[33m",
                "Blue": "\033[34m",
                "Magenta": "\033[35m",
                "Cyan": "\033[36m",
                "White": "\033[37m",
                "Bright Black": "\033[90m",
                "Bright Red": "\033[91m",
                "Bright Green": "\033[92m",
                "Bright Yellow": "\033[93m",
                "Bright Blue": "\033[94m",
                "Bright Magenta": "\033[95m",
                "Bright Cyan": "\033[96m",
                "Bright White": "\033[97m",
                "Dark Black": "\033[30;2m",
                "Dark Red": "\033[31;2m",
                "Dark Green": "\033[32;2m",
                "Dark Yellow": "\033[33;2m",
                "Dark Blue": "\033[34;2m",
                "Dark Magenta": "\033[35;2m",
                "Dark Cyan": "\033[36;2m",
                "Dark White": "\033[37;2m",
    }
    def init(self, mass, velocity, direction, position, pinned=False, name=None, color="\033[0m]", force=[0, 0]):
        """
        mass should be either a float or an integer
        velocity should be either a float or an integer
        direction should be either a float or an integer, indicating the degree between the line connecting the body and the origin and X + axis
        position should be a list of two items, indicating the coordinate of the body
        if a body is pinned, its position won't change
        name will be assigned with its number (plz correct me if the grammer here is terrible) if not specified
        color accepts a series of color names and you can also directly use RGB code connected with ";". e.g. color = "143;192;220". White if not specifed.
        force should be a list of two itmes, indicating how many newtons the force is and the direction of the force. e.g. force = [65536, 72]
        """
        global body_num
        self.num = body_num + 1
        self.name = name if name != None else self.num
        self.m = mass
        self.v = velocity
        self.d = direction
        self.p = position
        self.pinned = True if pinned == True else False
        self.color = Body.palette[color] if color in Body.palette else f"\033[38;2;{color}m"
        self.f = force

        
        
        body_num += 1



class Draw:
    def init(self,) -> None:
        width, height = get_terminal_size()
        pass



class Funcs:
    def __init__(self) -> None:
        pass

    def sin(x):
        return math.sin(x / 180 * math.pi)
    def cos(x):
        return math.cos(x / 180 * math.pi)
    def arcsin(x):
        return math.asin(x) / math.pi * 180
    def arccos(x):
        return math.acos(x) / math.pi * 180
    def universal_gravitation(m1,m2,r,G):
        return G * m1 * m2 / r ** 2
    def distance(a,b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    def resultant_force(f1, f2):
        component_force_x = f1[0] * Funcs.cos[f1[1]] + f2[0] * Funcs.cos[f2[1]]
        component_force_y = f1[0] * Funcs.sin[f1[1]] + f2[0] * Funcs.sin[f2[1]]
        

    


body_num = 0
gravitational_constant = 6.67430 * 10**-11
bodies = []
bodies.append(Body())

while True:
    for index_1, body_1 in enumerate(bodies):
        for body_2 in bodies[index_1+1:]:
            r = Funcs.distance(body_1.p,body_2.p)
            body_1.f = [Funcs.universal_gravitation(body_1.m, body_2.m, r, gravitational_constant), ]
            
            pass
