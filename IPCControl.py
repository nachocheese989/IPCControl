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
    cam = SWADS440(url=<url>)
    cam.basic_stream()
    ```
REMEMBER: the url field must be the url of the camera, and end in '/'.
"""
import platform
import keyboard
import command
import stream
import utils
import keycontrol
plat = platform.system()
if platform == "Windows":
    import joystick

print(plat)
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
    
    if plat == "Windows":
        def joystick_stream(self):
            """
            Control the camera with an xbox controller and show the camera stream (windows only).
            """
            cap = stream.videocapture(self.stream_url)
            joystick.connect_controller()
            while True:
                self.speed = joystick.joy_control(self.speedup, self.slowdown, self.speed)
                frame = stream.get_frame(cap, self.scaling)
                if stream.render_frame(frame, self.esc_key): break
            stream.destroy(cap)
        def joystick_control(self):
            """
            Control the camera with an xbox controller, no stream. (windows only)
            """
            joystick.connect_controller()
            while True:
                if keyboard.is_pressed(self.esc_key): break
                self.speed = joystick.joy_control(self.speedup, self.slowdown, self.speed)
    if plat != "Darwin":
        def keyboard_stream(self):
            """
            Control the camera with the keyboard, with stream.
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
        def keyboard_control(self):
            """
            Control the camera with the keyboard, no stream.
            """
            p_left = 0
            p_right = 0
            p_up = 0
            p_down = 0
            while True:
                if keyboard.is_pressed(self.esc_key): break
                self.speed, p_left, p_right, p_up, p_down = keycontrol.processkeys(self.left, self.right, self.up, self.down, self.speedup, self.slowdown, self.speed, p_left, p_right, p_up, p_down)

    def code_bool_control(self, left:bool=False, right:bool=False, up:bool=False, down:bool=False):
        """
        Control the camera with code, no stream.\n
        uses booleans to control the camera, one bool for each direction.
        """
        command.send_bool(left, right, up, down)
    def code_vec_control(self, vec:tuple[int, int]):
        """
        Control the camera with code, no stream.\n
        Uses a vector in the form of a tuple to control the camera.\n
        This simply checks if the x and y values are > or < than 0, then sends the appropriate boolean command.\n
        Rounding vectors should be done before calling this function, if required.
        """
        command.send_vec(vec)
    def update_speed(self, speed:int):
        """
        Update the speed of the camera.
        """
        self.speed = speed
        command.set_pt_rate(self.speed, self.settings_url)



# example function

def example():
    cam = SWADS440(url="http://admin:123456@192.168.1.15/")
    cam.keyboard_stream()

if __name__ == "__main__":
    example()