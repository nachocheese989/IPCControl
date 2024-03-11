"""
Useful classes and functions.\n
Includes:
    `vec2`: a 2D vector
    `CAMURL`: the url of the camera, change to whatever yours is.\n
    the url should be: `http://<username>:<password>@<ip>:<port>/` (default port is 80)
    `CameraError`: an custom error class, used for camera errors
"""
import math

CAMURL = "http://admin:123456@192.168.1.15/"

class vec2:
    def __init__(self, x=0, y=0) -> None: self.x = x; self.y = y
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
    def __truediv__(self, x):
        if isinstance(x, int) or isinstance(x, float):
            return vec2(self.x / x, self.y / x)
        if x is vec2:
            return vec2(self.x / x.x, self.y / x.y)
    def from_tup(t: tuple[float]): "Make a vec2 from a Tuple"; return vec2(t[0], t[1])
    def from_list(l: list[float]): "Make a vec2 from a List"; return vec2(l[0], l[1])


class CameraError(Exception):
    """An error with the camera"""
    def __init__(self, message:str, errors:tuple[str]=()) -> None:
        self.message = message
        self.errors = errors
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} {self.errors}"