"""
XInput only works on windows, macos does not agree with controllers and I'm not bothered to make one for linux.\n
So this only works on windows.
"""
import keyboard
import XInput as xi
import cv2
from stream import get_frame, STREAM_URL
from command import set_pt_rate, send_vec
from utils import vec2
import time

def main():
    connect_controller()
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

def connect_controller():
    if not xi.get_connected()[0]:
        print("Please connect a controller")
        while not xi.get_connected()[0]: time.sleep(1)
    print("Controller connected")

def joy_control(speedup:str='w', slowdown:str='s', s:int=3) -> tuple[int, bool]:
    if not xi.get_connected()[0]: print("Controller Disconnected"); return s, True
    if keyboard.is_pressed(speedup):
        s = max(min(s+1, 10), 0)
        set_pt_rate(s)
    if keyboard.is_pressed(slowdown):
        s = max(min(s-1, 10), 0)
        set_pt_rate(s)
    state = xi.get_state(0)
    vec: vec2 = vec2.from_tup(xi.get_thumb_values(state)[0])
    send_vec(vec.r().t())
    return s, False



if __name__ == "__main__":
    main()