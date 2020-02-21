from grove_rgb_lcd import *
from grovepi import *
from pad4pi import rpi_gpio 
import time 
import sys 
import requests 
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

entered_passcode = ""
correct_passcode = "1234"
def cleanup():
    global keypad
    keypad.cleanup()
    print("asd")
def correct_passcode_entered():
    led = 4
    pinMode(led,"OUTPUT")
    try:	
        digitalWrite(led,1)             # Send HIGH to switch on LED
        print ("moving...")
        time.sleep(15)

        digitalWrite(led,0)             # Send LOW to switch off LED
        print ("done")

    except KeyboardInterrupt:   # Turn LED off before stopping
        digitalWrite(led,0)
    except IOError:                             # Print "Error" if communication error encountered
        print ("Error")		      
#    cleanup()
def incorrect_passcode_entered():
    print("Incorrect passcode. Access denied.")
    global entered_passcode, correct_passcode
    entered_passcode = ""

def digit_entered(key):
    global entered_passcode, correct_passcode

    entered_passcode += str(key)
    setText(str(entered_passcode))
    print(entered_passcode)
def non_digit_entered(key):
    global entered_passcode

    if key == "*" and len(entered_passcode) > 0:
        entered_passcode = entered_passcode[:-1]
        setText(str(entered_passcode))
        print(entered_passcode)
    else:
        print(entered_passcode)
        session = requests.Session()
        data = {
           'key':str(entered_passcode)
        }
        r = session.post('http://127.0.0.1:5000/check_key',data=data)
        print(r.text)
        if(str(r.text)=="true"):
            correct_passcode_entered()
        else:
            incorrect_passcode_entered()
def key_pressed(key):
    print(key)
    try:
        int_key = int(key)
        if int_key >= 0 and int_key <= 9:
            digit_entered(key)
    except ValueError:
        non_digit_entered(key)

