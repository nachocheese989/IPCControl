"""
Control the camera with the keyboard.\n
The `arrowkeycontrol()` function is a quick way to control the camera with the arrow keys.
"""
import stream
from command import *
import keyboard
import cv2

def processkeys(left:str, right:str, up:str, down:str, speedup:str, speeddown:str, s:int=3, p_left:int=0, p_right:int=0, p_up:int=0, p_down:int=0) -> tuple[int, int, int, int, int]:
    """
    Send keypresses to the server.\n
    `left`, `right`, `up`, `down`, `speedup`, `speeddown` are all strings, representing the keys to be pressed.\n
    `s` is the current speed of the camera, `p_left`, `p_right`, `p_up`, `p_down` are the previous states of the direction keys.\n
    `processkeys() -> (new_speed, new_p_left, new_p_right, new_p_up, new_p_down)`\n
    e.g usage:
    ```
    left = "left"
    right = "right"
    up = "up"
    down = "down"
    speedup = "w"
    speeddown = "s"
    s = 3
    p_left = 0
    p_right = 0
    p_up = 0
    p_down = 0
    while True:
        s, p_left, p_right, p_up, p_down = processkeys(left, right, up, down, speedup, speeddown, s, p_left, p_right, p_up, p_down)
    ```
    """
    if keyboard.is_pressed(speedup):
        s = max(min(s+1, 10), 0)
        set_pt_rate(s)
    if keyboard.is_pressed(speeddown):
        s = max(min(s-1, 10), 0)
        set_pt_rate(s)
    l = keyboard.is_pressed("left")
    r = keyboard.is_pressed("right")
    u = keyboard.is_pressed("up")
    d = keyboard.is_pressed("down")
    if l != p_left or r != p_right or u != p_up or d != p_down:
        send_bool(l, r, u, d)
    p_l = left
    p_r = right
    p_u = up
    p_d = down
    return (s, p_l, p_r, p_u, p_d)

def arrowkeycontrol():
    s = 3
    left=0
    right=0
    up=0
    down=0
    p_left = 0
    p_right = 0
    p_up = 0
    p_down = 0
    cap = cv2.VideoCapture(stream.STREAM_URL)
    while True:
        if keyboard.is_pressed("w"):
            s = max(min(s+1, 10), 0)
            set_pt_rate(s)
        if keyboard.is_pressed("s"):
            s = max(min(s-1, 10), 0)
            set_pt_rate(s)
        left = keyboard.is_pressed("left")
        right = keyboard.is_pressed("right")
        up = keyboard.is_pressed("up")
        down = keyboard.is_pressed("down")
        if left != p_left or right != p_right or up != p_up or down != p_down:
            send_bool(left, right, up, down)
        p_left = left
        p_right = right
        p_up = up
        p_down = down
        ret, frame = stream.get_frame(cap, scaling=2)
        cv2.imshow('Capturing, Q to quit',frame)
        #cheap fix to opencv freezing when a key is held
        do_stop = False
        while True:
            key = cv2.waitKey(1)
            if key == -1: 
                break
            if key == ord('q'):
                do_stop = True
                
        if do_stop:
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    arrowkeycontrol()