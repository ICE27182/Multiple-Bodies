

import math
from threading import Thread
from shutil import get_terminal_size
from time import sleep
try:
    import msvcrt
    key_capture = True
except ModuleNotFoundError:
    key_capture = False

from os import system
system("cls")


class Body:
    """
    A body has following attributes:
        num - int - number
        name - str - name
        m - float/int(kg) - mass
        v - list [float/int, float/int](m/s) - velocity in two directions
        p - list [float/int, float/int](m) - postion
        r - float/int(kg) - radius
        pinned - bool - if a body is pinned, its position won't change
        color - str - color
        ring -list [float/int, float/int](m) - whether the astronomical object has a ring around it and what its inside and outside radiuses are. [0, 0] if it doesn't have one.
        f - list [float/int, float/int](N) - force in two directions
    """
    palette = {
                "Black": "\033[30m██",
                "Red": "\033[31m██",
                "Green": "\033[32m██",
                "Yellow": "\033[33m██",
                "Blue": "\033[34m██",
                "Magenta": "\033[35m██",
                "Cyan": "\033[36m██",
                "White": "\033[37m██",
                "Bright Black": "\033[90m██",
                "Bright Red": "\033[91m██",
                "Bright Green": "\033[92m██",
                "Bright Yellow": "\033[93m██",
                "Bright Blue": "\033[94m██",
                "Bright Magenta": "\033[95m██",
                "Bright Cyan": "\033[96m██",
                "Bright White": "\033[97m██",
                "Dark Black": "\033[30;2m██",
                "Dark Red": "\033[31;2m██",
                "Dark Green": "\033[32;2m██",
                "Dark Yellow": "\033[33;2m██",
                "Dark Blue": "\033[34;2m██",
                "Dark Magenta": "\033[35;2m██",
                "Dark Cyan": "\033[36;2m██",
                "Dark White": "\033[37;2m██",
              }
    
    def __init__(self, mass, velocity, direction, position, radius, pinned=False, name=None, color="\033[0m]", ring=[0,0], force=[0, 0]) -> None:
        """
        mass should be either a float or an integer
        velocity should be either a float or an integer
        direction should be either a float or an integer, indicating the degree between the line connecting the body and the origin and X + axis
        position should be a list of two items, indicating the coordinate of the body
        radius should be a float or an integer
        if a body is pinned, its position won't change
        name will be assigned with its number (plz correct me if the grammer here is terrible) if not specified
        color accepts a series of color names and you can also directly use RGB code connected with ";". e.g. color = "143;192;220". White if not specifed.
        force should be a list of two itmes, indicating how many newtons the forces are in the direction of x and y. e.g. force = [10, -2]; or it can be a tuple, indicating the polar cooridinate of the force
        """
        global body_num
        self.num = body_num + 1
        self.name = name if name != None else self.num
        self.m = mass
        self.v = Funcs.pol2rec(velocity, direction)
        self.p = position
        self.r = radius
        self.pinned = True if pinned == True else False
        self.color = Body.palette[color] if color in Body.palette else f"\033[38;2;{color}m"
        self.ring = ring
        self.f = force if type(force) == list else Funcs.pol2rec(force[0], force[1])
        body_num += 1



class Display:
    def __init__(self, gravity_map=False, info=True, ln=False) -> None:
        width, height = get_terminal_size()
        width = width // 4 * 2  - 5
        height = height // 2 * 2 - 7
        print("\033[F" * (height + 20))
        pos_range = ((cam[0] - width // 2 * scale, cam[1] - height // 2 * scale), (cam[0] + width // 2 * scale, cam[1] + height // 2 * scale))
        frame = {y:{} for y in range(height)}
        if gravity_map == True:
            frame = Display.gravity_map(frame, pos_range, width, height, ln)
        Display.draw(Display.get_frame(frame, pos_range, width, height), width, height)
        if info == True:
            Display.info(width,height)

    def gravity_map(frame, pos_range, width, height, ln=False):
        gravity_val = [[0 for _ in range(width)] for _ in range(height)]
        max_val, min_val = 0, 0
        for y in range(height):
            for x in range(width):
                for body in bodies:
                    d = d if (d := Funcs.distance(((x - 0.5) * scale + pos_range[0][0], (y - 0.5) * scale + pos_range[0][1],), body.p)) != 0 else 1
                    g = gravitational_constant * body.m / body.r**2
                    if ln == False:
                        gravity_val[y][x] += min(Funcs.universal_gravitation(body.m, 1, d, gravitational_constant), g)
                    else:
                        gravity_val[y][x] += math.log(min(Funcs.universal_gravitation(body.m, 1, d, gravitational_constant), g), math.e)
            max_val, min_val = max(max(gravity_val[y]), max_val), min(min(gravity_val[y]), min_val)
        step = (max_val - min_val) / 512
        for y in range(height):
            for x in range(width):
                frame[y][x] = Funcs.pseudo_color512((min(int((gravity_val[y][x] - min_val) // step), 511)))
        return frame



    def get_frame(frame, pos_range, width, height):
        for body in bodies:
            if pos_range[0][0] < body.p[0] < pos_range[1][0] and pos_range[0][1] < body.p[1] < pos_range[1][1]:
                # Relative coordiantes
                pos = ((body.p[0] - pos_range[0][0]) / scale, (body.p[1] - pos_range[0][1]) / scale)
                r = body.r / scale
                ring_in, ring_out = body.ring[0] / scale, body.ring[1] / scale
                frame[math.ceil(pos[1])][math.ceil(pos[0])] = body.color
                # Here the larger number is added 2 rather than 1 due to accuracy issue
                for y in range(int(pos[1] - max(r, ring_out)), int(pos[1] + max(r, ring_out) + 2)):
                    for x in range(int(pos[0] - max(r, ring_out)), int(pos[0] + max(r, ring_out) + 2)):
                        d = Funcs.distance((x - 0.5, y - 0.5), pos)
                        if ( d <= r or ring_in <= d <= ring_out) and 0 <= x < width and 0 <= y < height:
                            frame[y][x] = body.color
        return frame
    
    def info(width,height):
        body = bodies[cam[3] % len(bodies)]
        v,vd = Funcs.rec2pol(body.v[0], body.v[1])
        a,ad = Funcs.rec2pol(body.f[0] / body.m, body.f[1]/ body.m)
        print(f"name:{body.name}   number:{body.num}   color:{body.color}\033[0m   mass:{body.m:E}kg    velocity:{v:E}m/s   Vdirection:{vd:.3f}°   acceleration:{a:E}m/s²   Adirection:{ad:.3f}°   position:{body.p[0]/au:.3f} {body.p[1]/au:.3f}(au)     "
            + f"\nWidth:{width}   Height:{height}   scale(in au):{scale/au:.6f}   cam:{cam[0]/au:.3f} {cam[1]/au:.3f}(au)\n")


    def draw(frame, width, height,):
        img = []
        for y in range(height - 1, -1, -1):
            for x in range(width):
                img.append(f"{frame[y][x]}\033[0m" if x in frame[y]  else "  ")
            img.append("\n")
        print("".join(img))



class Funcs:
    def __init__(self) -> None:
        pass

    def sin(x) -> float:
        return math.sin(x / 180 * math.pi)
    def cos(x) -> float:
        return math.cos(x / 180 * math.pi)
    def arcsin(x) -> float:
        return math.asin(x) / math.pi * 180
    def arccos(x) -> float:
        return math.acos(x) / math.pi * 180
    def arctan(x) -> float:
        return math.atan(x) / math.pi * 180
    def universal_gravitation(m1,m2,r,G) -> float:
        return G * m1 * m2 / r ** 2
    def distance(a,b) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    def pol2rec(r, theta):
        return [r * Funcs.cos(theta), r * Funcs.sin(theta)]
    def rec2pol(v,u):
        if v == 0:
            return [abs(u), 90*u/abs(u) if u != 0 else 0]
        return [math.sqrt(v**2 + u**2), Funcs.arctan(u/v) if v > 0 else Funcs.angle_in_range(Funcs.arctan(u/v) - 180)]
    def angle_in_range(theta):
        return (theta + 180) % 360 - 180
    def resultant_force(f1, f2):
        """f1, f2: [float/int, float/int](N)"""
        return [f1[0] + f2[0], f1[1] + f2[1]]
    def pseudo_color512(val:int,char="██"):
        if val < 256:
            return f"\033[38;2;0;{val//2};{val}m██\033[0m"
        else:
            return f"\033[38;2;{val-256};{val//2};{511-val}m██\033[0m"
    def circle_orbit_velocity(mass, radius):
        return math.sqrt(gravitational_constant * mass / radius)
    
    
        
class Input:
    def __init__(self) -> None:
        if key_capture == True:
            Thread(target=Input.keyboard_input,daemon=True).start()
        pass

    def keyboard_input():
        global key, cam
        from winsound import Beep
        while True:
            key = msvcrt.getwch()
            if key == "w":
                cam[1] += scale
            elif key == "s":
                cam[1] -= scale
            elif key == "a":
                cam[0] -= scale
            elif key == "d":
                cam[0] += scale
            

            elif key == "l":
                cam[2] = not cam[2]
            elif key == "[":
                cam[3] -= 1
            elif key == "]":
                cam[3] += 1

            elif key == "Q":
                exit(0)
                



au = 149597870700
scale = 1.495978707*10**10
seconds_per_frame = 3600 * 12
gravitational_constant = 6.67430 * 10**-11
Input()
key = None
cam = [0,0,False,0]
body_num = 0
bodies = []
bodies.append(Body(1.9885 *10**30, 0, 0, [0,0], 6.957*10**8, pinned=False, color="Dark Red", name = "Sun"))
bodies.append(Body(5.972*10**24, Funcs.circle_orbit_velocity(2*10**30, au), 90, [au, 0], 6.378*10**6, pinned=False, color="Dark Blue"))
# bodies.append(Body(2.5*10**23, Funcs.circle_orbit_velocity(2*10**30, 0.5*au), 0, [0,0.5*au], 5*10**7, pinned=False, color="Dark Green",))
# bodies.append(Body(2.5*10**18, 50000, 0, [0.25*au,0.25*au], 5*10**7, pinned=False, color="Cyan",))
bodies.append(Body(5.6834 * 10**26, Funcs.circle_orbit_velocity(1.9885 *10**30, 9.5826 *au), 180, [0, 9.5826 *au], 58232000, name="Saturn", color="Dark Yellow", ring=[7*10**6 + 58232000, 80*10**6 + 58232000]))

gravity_map = True
pause = False
ln = False
info = True

# Physics
while key != "Q":
    

    if pause == False:
        # Calculate the force each body takes
        # O(n!) :(
        for body in bodies:
            body.f = [0, 0]
        for index_1, body_1 in enumerate(bodies):
            for body_2 in bodies[index_1+1:]:
                r = Funcs.distance(body_1.p,body_2.p)
                gravitation = Funcs.universal_gravitation(body_1.m, body_2.m, r, gravitational_constant)
                f_1 = (gravitation / r * (body_2.p[0] - body_1.p[0]), gravitation / r * (body_2.p[1] - body_1.p[1]))
                body_1.f = [body_1.f[0] + f_1[0], body_1.f[1] + f_1[1]]
                body_2.f = [body_2.f[0] - f_1[0], body_2.f[1] - f_1[1]]
        for body in bodies:
            if body.pinned == False:
                body.v = [
                            body.v[0] + body.f[0] / body.m * seconds_per_frame, 
                            body.v[1] + body.f[1] / body.m * seconds_per_frame,
                         ]
                body.p = [
                            body.p[0] + body.v[0] * seconds_per_frame, 
                            body.p[1] + body.v[1] * seconds_per_frame,
                         ]
                
    if cam[2] == True:
        cam = bodies[cam[3] % len(bodies)].p + cam[2:]        

    Display(gravity_map,info,ln)

    
    if key == ".":
        seconds_per_frame *= 2
        key = None
    elif key == ",":
        seconds_per_frame /= 2
        key = None
    elif key == "/":
        seconds_per_frame = 3600 * 24
        key = None

    elif key == "E":
        ln = not ln
        key = None
    
    elif key == "i":
        info = not info
        system("cls")
        print("")   # Idk the principle, but it works
        key = None

    elif key == "e":
        scale /= 2
        key = None
    elif key == "f":
        scale *= 2
        key = None
        
    elif key == "G":
        gravity_map = not gravity_map
        key = None
    elif key == " ":
        pause = not pause
        key = None


