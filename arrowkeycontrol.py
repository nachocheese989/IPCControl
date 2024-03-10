import stream
from pynput.keyboard import Listener
from command import *

STREAM_URL = "http://admin:123456@192.168.1.15:80/videostream.cgi"
left=0
right=0
up=0
down=0

def on_press(key):
    global left, right, up, down
    if str(key).replace("'", "") == "q":
        listener.stop()
    if str(key).replace("'", "") == "e":
        send(11)
    match str(key).replace("'", ""):
        case "Key.right":
            right = 1
            send_bool(left, right, up, down)
        case "Key.left":
            left = 1
            send_bool(left, right, up, down)
        case "Key.up":
            up = 1
            send_bool(left, right, up, down)
        case "Key.down":
            down = 1
            send_bool(left, right, up, down)

def on_release(key):
    global left, right, up, down
    match str(key).replace("'", ""):
        case "Key.right":
            right = 0
            send_bool(left, right, up, down)
        case "Key.left":
            left = 0
            send_bool(left, right, up, down)
        case "Key.up":
            up = 0
            send_bool(left, right, up, down)
        case "Key.down":
            down = 0
            send_bool(left, right, up, down)




listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
stream.stream()
listener.stop()
# listener.join()