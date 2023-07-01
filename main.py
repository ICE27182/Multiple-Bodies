

import math
from shutil import get_terminal_size



class Body:
    def init(self, mass, velocity, facing, position, pinned=False, name=None, color=None):
        global body_num
        self.num = body_num + 1
        self.name = name if name != None else self.num
        self.m = mass
        self.v = velocity
        self.f = facing
        self.p = position
        self.pinned = True if pinned = True else False
        
        body_num += 1


class Draw:
    def init(self,) -> None:
        width, height = get_terminal_size()
        pass

body_num = 0
