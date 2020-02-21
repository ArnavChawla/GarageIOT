from pad4pi import rpi_gpio
import requests
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [12, 6, 13, 19] # BCM numbering
COL_PINS = [16, 20, 21] # BCM numbering

factory = rpi_gpio.KeypadFactory()
factory.create_4create_4_by_3_keypad
# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
pin = ""
lastbutton = ""

def printKey(key):
    print(key)
    lastbutton = key
    if(key != "#"):
        pin+=key

# printKey will be called each time a keypad button is pressed
while(True):
    keypad.registerKeyPressHandler(printKey)
    if(lastbutton == "#"):
        intpin = int(pin)
        session = requests.Session()
        data = {
            'key':intpin
        }
        r = session.post("http://127.0.0.1:5000/check_key",data=data)
        if(r.text==True):
            #do the garage stuff
