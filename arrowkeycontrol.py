import stream
from command import *
import keyboard
import cv2

def main():
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
        ret, frame = cap.read()
        width = 1500
        height = 1080
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
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
    main()