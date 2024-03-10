from Gamepad.Gamepad import *
import time

class vec2:
    def __init__(self, x=0, y=0) -> None: self.x = x;self.y = y
    def m(self) -> float: """Return magnitude of vector"""; return math.sqrt(self.x**2+self.y**2)
    def t(self) -> tuple[float]: """Return vector as a tuple"""; return (self.x, self.y)
    def r(self): """Return a rounded vector"""; return vec2(round(self.x), round(self.y))
    def __add__(self, x):
        if isinstance(x, int) or isinstance(x, float):
            return vec2(self.x + x, self.y + x)
        if x is vec2:
            return vec2(self.x + x.x, self.y + x.y)
        
    def __str__(self):
        return f"vec2({self.x}, {self.y})"

SIDE='LEFT'
type=XboxONE

AXIS_X=SIDE+'-X'
AXIS_Y=SIDE+'-Y'

# if not available():
#     print('Please connect your gamepad...')
#     while not available():
#         time.sleep(1.0)
gamepad = type()

gamepad.startBackgroundUpdates()

# from inputs import devices

# for device in devices:
#     print(device)