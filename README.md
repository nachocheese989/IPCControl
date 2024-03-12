# SWADS-440IPC controller

I hate this camera.

Dependencies:
    pynput, xinput-python (windows only), keyboard, opencv-python, requests, pynput, sys, math, time

just `pip install` them manually, or copy/paste the below into a .txt file and run `pip install -r <path_to_file>`:
```
pynput
xinput-python
keyboard
opencv-python
requests
pynput
sys
math
time
```

## Installation

    cd <where its going>
    git clone https://github.com/nachocheese989/IPCControl

That's it.
You can access it by putting the IPControl.py path in you PYTHONPATH env variable (I think?) and importing it as `import IPCControl`.
More simply you can put the IPCControl directory in you project directory, then importing it as `import IPCControl.IPCConrol`

## Usage

The docs in the python files explain it. Run IPCControl.py, changing the url to your cameras ip for an example.
