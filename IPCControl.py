"""
Main script to control the SWADS-440 IP camera.\n
I hate this camera.\n
It can only be controlled through sending commands to a cgi script on the camera server.\n
This was a pain. You'll have to actually find out the ip of the camera, I found mine in the router menu.\n
It took ages to look in the source section in the inspect element tab to find the cgi script and variables.\n
Things in this:
    `utils` provides useful classes and functions.\n
    `keycontrol` provides a way to control the camera with the keyboard.\n
    `stream` provides methods of viewing the camera stream, and processing the images.\n
    `command` provides methods of sending commands to the camera.\n
    `joystick` provides a way to control the camera with an xbox controller (only on windows)\n
    `SWADS440` is the main class to control the camera.\n
e.g usage:
    ```
    # do a basic stream, no controls
    from IPCControl import SWADS440
    cam = SWADS440(<settings>)
    cam.basic_stream()
    ```
"""
import platform, sys
import command
import stream
import utils
import keycontrol
platform = platform.system()
if platform == "Windows":
    import joystick


class SWADS440:
    """
    A class to control the SWADS-440 camera.\n
    """
    def __init__(self, speed:int=3, keys:list[str]=['left', 'right', 'up', 'down', 'w', 's'], esc_key:str='q', scaling:int=2, url:str=utils.CAMURL) -> None:
        """
        Create a new camera object.\n
        `speed`: the speed of the camera\n
        `keys`: the keys to control the camera\n
        keys should be in the order [
            left,
            right,
            up,
            down,
            speedup,
            slowdown
        ]
        `esc_key`: press this to quit a stream
        `scaling`: the factor to scale the image by
        `url`: the url of the camera. The default is CAMURL in utils.py
        """
        self.url = url
        self.stream_url = url+"video.cgi"
        self.command_url = url+"decoder_control.cgi"
        self.settings_url = url+"set_misc.cgi"
        self.speed = speed
        self.curr_speed = speed
        self.left = keys[0]
        self.right = keys[1]
        self.up = keys[2]
        self.down = keys[3]
        self.speedup = keys[4]
        self.slowdown = keys[5]
        self.esc_key = esc_key
        self.scaling = scaling
    def basic_stream(self):
        """
        A basic stream of the camera, no controls.
        """
        stream.stream(self.scaling, self.esc_key)
    def keyboard_stream(self):
        """
        Control the camera with the keyboard.
        """
        cap = stream.videocapture(self.stream_url)
        p_left = 0
        p_right = 0
        p_up = 0
        p_down = 0
        while True:
            self.speed, p_left, p_right, p_up, p_down = keycontrol.processkeys(self.left, self.right, self.up, self.down, self.speedup, self.slowdown, self.speed, p_left, p_right, p_up, p_down)
            frame = stream.get_frame(cap, self.scaling)
            if stream.render_frame(frame, self.esc_key): break
        stream.destroy(cap)
    if platform == "Windows":
        def joystick_stream(self):
            """
            Control the camera with an xbox controller (windows only)
            """
            cap = stream.videocapture(self.stream_url)
            joystick.connect_controller()
            while True:
                self.speed = joystick.joy_control(self.speedup, self.slowdown, self.speed)
                frame = stream.get_frame(cap, self.scaling)
                if stream.render_frame(frame, self.esc_key): break
            stream.destroy(cap)




SWADS440().joystick_stream()


