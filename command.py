import requests

STOP = 1
DOWN = 0
UP = 2
RIGHT = 4
LEFT = 6
RIGHT_DOWN = 90
LEFT_DOWN = 91
RIGHT_UP = 92
LEFT_UP = 93

COMMAND_URL="http://admin:123456@192.168.1.15/decoder_control.cgi"

SETTINGS_URL = "http://admin:123456@192.168.1.15/set_misc.cgi?led_mode=1&ptz_disable_preset=1&ptz_patrol_h_rounds=1&ptz_patrol_v_rounds=1&ptz_patrol_rate=1"

def change_settings(settings, debug = False):
    if debug:
        print("settings: ", settings)
        print("response: ", requests.get(url=SETTINGS_URL, params=settings))
    else:
        requests.get(url=SETTINGS_URL, params=settings)

def send(c:int=1, debug = False):
    if debug: 
        print("command: ", c)
        print("response: ", requests.get(url=COMMAND_URL, params={"command":c}))
    else:
        requests.get(url=COMMAND_URL, params={"command":c})

def stop():
    send(STOP)

# &ptz_patrol_up_rate=5&ptz_patrol_down_rate=5&ptz_patrol_left_rate=5&ptz_patrol_right_rate=5
change_settings({
    "ptz_patrol_up_rate":"10",
    "ptz_patrol_down_rate": "10",
    "ptz_patrol_left_rate": "10",
    "ptz_patrol_right_rate": "10"
}, True)