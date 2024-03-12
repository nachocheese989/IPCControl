"""
Arrow key control for MacOS, the keyboard.is_pressed() requires admin priveleges while pynput doesn't
"""
import stream
from pynput.keyboard import Listener
from command import *

STREAM_URL = "http://admin:123456@192.168.1.15:80/videostream.cgi"
left=0
right=0
up=0
down=0

p_left=0
p_right=0
p_up=0
p_down=0

def update():
    global left, right, up, down

    if left and right:
        left, right = 0,0
    if up and down:
        up, down = 0,0
    
    if left == 0 and right == 0 and up == 0 and down == 0:
        send(STOP)
    else:
        if right and down:
            send(RIGHT_DOWN)
        elif left and down:
            send(LEFT_DOWN)
        elif right and up:
            send(RIGHT_UP)
        elif left and up:
            send(LEFT_UP)
        else:
            if left: send(LEFT)
            if right: send(RIGHT)
            if up: send(UP)
            if down: send(DOWN)

def on_press(key):
    global left, right, up, down
    if str(key).replace("'", "") == "q":
        listener.stop()
    if str(key).replace("'", "") == "e":
        send(11)
    match str(key).replace("'", ""):
        case "Key.right":
            right = 1
            update()
        case "Key.left":
            left = 1
            update()
        case "Key.up":
            up = 1
            update()
        case "Key.down":
            down = 1
            update()

def on_release(key):
    global left, right, up, down
    match str(key).replace("'", ""):
        case "Key.right":
            right = 0
            update()
        case "Key.left":
            left = 0
            update()
        case "Key.up":
            up = 0
            update()
        case "Key.down":
            down = 0
            update()




listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
stream.stream()
listener.stop()
# listener.join()