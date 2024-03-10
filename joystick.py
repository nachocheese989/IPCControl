import keyboard
import XInput as xi
import cv2
from stream import get_frame, STREAM_URL
from command import set_pt_rate, send_vec
import math
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
    def __mul__(self, x):
        if isinstance(x, int) or isinstance(x, float):
            return vec2(self.x * x, self.y * x)
        if x is vec2:
            return vec2(self.x * x.x, self.y * x.y)

    def from_tup(t: tuple[float]): return vec2(t[0], t[1])

if not xi.get_connected()[0]:
    while not xi.get_connected()[0]: print("Please connect a controller")
    print("Controller connected")

cap = cv2.VideoCapture(STREAM_URL)
p_v = vec2(0, 0)
s = 2
while True:
    if keyboard.is_pressed("q"):
        break
    if keyboard.is_pressed("w"):
        s = max(min(s+1, 10), 0)
        set_pt_rate(s)
    if keyboard.is_pressed("s"):
        s = max(min(s-1, 10), 0)
        set_pt_rate(s)
    if not xi.get_connected()[0]: print("Controller Disconnected"); break
    state = xi.get_state(0)
    vec: vec2 = vec2.from_tup(xi.get_thumb_values(state)[0])
    if (vec * 10).r() != p_v:
        p_v = (vec * 10).r()
        send_vec(vec.r().t())
    ret, frame = get_frame(cap)
    cv2.imshow('Capturing, Q to quit',frame)
    do_stop = False
    while True:
        key = cv2.waitKey(1)
        if key == -1: # no keycode reported
            break # inner loop
        if key == ord('q'):
            do_stop = True # break outer loop
            # don't break inner loop yet, we'll do that in the next iteration when no keycode is reported
    if do_stop:
        break
cap.release()
cv2.destroyAllWindows()

print("end")