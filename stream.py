"""
Stuff to do with streaming the camera
"""
import cv2, sys
from utils import CAMURL, CameraError

STREAM_URL = CAMURL+"video.cgi"

SCALE = (640, 480)

def stream(scaling=2, esc_key:str='q'):
    """
    Basic stream of the camera. No fancy shit. Press `esc_key` (default q) to quit
    """
    cap = cv2.VideoCapture(STREAM_URL)
    while True:
        ret, frame = get_frame(cap, scaling)
        if not ret: raise CameraError("Uh oh. The camera didn't return an image!")
        if render_frame(frame, esc_key): break
    cap.release()
    cv2.destroyAllWindows()

def destroy(cap: cv2.VideoCapture):
    """End the cv2 capture and destroy the window"""
    cap.release()
    cv2.destroyAllWindows()

def get_frame(cap: cv2.VideoCapture, scaling=1) -> cv2.VideoCapture:
    """
    Get a frame from the videocapture
    `cap`: the videocapture
    `scaling`: the amount to scale the frame by
    """
    ret, frame = cap.read()
    dim = (SCALE[0]*scaling, SCALE[1]*scaling)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    if not ret: raise CameraError("Uh oh. The camera didn't return an image!")
    return frame

def render_frame(frame, esc_key:str='q') -> bool:
    """
    Render the frame and return True if `esc_key` is pressed
    `frame`: the frame to render
    `esc_key`: return true if this key is pressed\n
    e.g usage along with other functions:
    ```
    cap = videocapture(STREAM_URL) # get the cv2.VideoCapture
    while True:
        ret, frame = get_frame(cap, 2) # get the frame
        if render_frame(frame, 'q'): # render the frame and break the loop if 'q' is pressed
            break
    """
    cv2.imshow(f"Capturing, {esc_key.upper()} to quit",frame)
    #cheap fix to opencv freezing when a key is held
    do_stop = False
    while True:
        key = cv2.waitKey(1)
        if key == -1: 
            break
        if key == ord(esc_key):
            do_stop = True
            
    return do_stop

def uniform_scale(frame, scaling:int, init_size=SCALE):
    """
    Uniformly scale a frame
    `frame`: the frame to scale
    `scaling`: the scaling factor
    `init_size`: the initial size of the frame
    """
    dim = (init_size[0]*scaling, init_size[1]*scaling)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def videocapture(url:str=STREAM_URL) -> cv2.VideoCapture:
    """
    Return a cv2.VideoCapture object
    """
    return cv2.VideoCapture(url)

if __name__ == "__main__":
    stream()