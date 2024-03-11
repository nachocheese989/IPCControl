import requests
from utils import CAMURL

STOP = 1
DOWN = 0
UP = 2
RIGHT = 4
LEFT = 6
RIGHT_DOWN = 90
LEFT_DOWN = 91
RIGHT_UP = 92
LEFT_UP = 93

COMMAND_URL = CAMURL+"decoder_control.cgi"

SETTINGS_URL = CAMURL+"set_misc.cgi"

def change_settings(settings, debug = False) -> None:
    """
    Change misc settings (Advanced>Other Settings from normal web view)
    """
    if debug:
        print("settings: ", settings)
        print("response: ", requests.get(url=SETTINGS_URL, params=settings))
    else:
        requests.get(url=SETTINGS_URL, params=settings)

def send(c:int=1, url:str=COMMAND_URL, debug:bool=False) -> None:
    """
    Sends the command 'c' to the camera.
    Prints camera response if debug is True
    """
    if debug: 
        print("response: ", requests.get(url=COMMAND_URL, params={"command":c}))
    else:
        requests.get(url=COMMAND_URL, params={"command":c})

def stop():
    send(STOP)

def set_pt_rate(rate:int, url:str=SETTINGS_URL, debug:bool=False):
    """
    Set the pan/tilt speed to an int between 0 and 10. Prints camera response if debug is True.
    """
    if rate > 10 or rate < 0:
        print("pt rate should be between 0 and 10, value has been clamped.")
    r = max(min(10-round(rate), 10), 0)
    if debug:
        print("response: ", requests.get(url=SETTINGS_URL, params={"ptz_patrol_rate": r}))
    else:
        requests.get(url=SETTINGS_URL, params={"ptz_patrol_rate": r})


def send_bool(l:bool, r:bool, u:bool, d:bool, url:str=COMMAND_URL, debug:bool=False) -> None:
    """
    Convert four directions (e.g, arrow keys) to a command, then send it to the camera
    """
    left = l
    right = r
    up = u
    down = d
    if left and right:
        left = 0
        right = 0
    if up and down:
        up = 0
        down = 0
    
    if left == 0 and right == 0 and up == 0 and down == 0:
        send(STOP, url, debug)
    else:
        if right and down:
            send(RIGHT_DOWN,url,  debug)
        elif left and down:
            send(LEFT_DOWN, url, debug)
        elif right and up:
            send(RIGHT_UP, url, debug)
        elif left and up:
            send(LEFT_UP, url, debug)
        else:
            if left: send(LEFT, url, debug)
            if right: send(RIGHT, url, debug)
            if up: send(UP, debug)
            if down: send(DOWN, url, debug)

def send_vec(vec:tuple[int], debug = False) -> None:
    """
    Send a vector to the camera. The vector is a tuple of two numbers, (x, y)
    """
    l = 0
    r = 0
    u = 0
    d = 0
    if vec[0] > 0: r = 1
    if vec[0] < 0: l = 1
    if vec[1] > 0: u = 1
    if vec[1] < 0: d = 1
    send_bool(l, r, u, d, debug)