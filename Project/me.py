import RPi.GPIO as GPIO
import time
import subprocess
import obstacle
import facialr
import sys
import objects
import obs
import obstaclefrontdemo
import obstaclebehinddemo

# these GPIO pins are connected to the keypad
# change these according to your connections!
L1 = 25
L2 = 8
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

choice = ""

# Initialize the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column


def readChoice(line, characters, choice):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        choice = characters[0]

    if GPIO.input(C2) == 1:
        choice = characters[1]

    if GPIO.input(C3) == 1:
        choice = characters[2]

    if GPIO.input(C4) == 1:
        choice = characters[3]

    GPIO.output(line, GPIO.LOW)
    return choice


# function to control the menu
def get_first_choice():
    
    time.sleep(3)
    print("Enter choice")
    subprocess.Popen(['espeak',"Enter your prefered choice"]).wait()
    time.sleep(3)
    choice = ""
    while True:
        choice = readChoice(L1, ["1", "2", "3", "A"], choice)
        choice = readChoice(L2, ["4", "5", "6", "B"], choice)
        choice = readChoice(L3, ["7", "8", "9", "C"], choice)
        choice = readChoice(L4, ["*", "0", "#", "D"], choice)
        if len(choice) == 1:
            if choice == "1":
                time.sleep(3)
                subprocess.Popen(["espeak", "starting obstacle detection in the front"]).wait()
                time.sleep(3)
                print("starting obstacle detection in the front")
                obstaclefrontdemo.start_obstacle_front()
                get_first_choice()
                break

            elif choice == "2":
                time.sleep(3)
                subprocess.Popen(["espeak", "stoping obstacle detection in the front"]).wait()
                time.sleep(3)
                print("stoping obstacle detection in the front")
                obstaclefrontdemo.stop_obstacle_front()
                get_first_choice()
                break

            elif choice == "3":
                time.sleep(3)
                subprocess.Popen(["espeak", "starting object identification"]).wait()
                time.sleep(3)
                print("starting object identification ")
                objects.start_object_detection()
                get_first_choice()
                break

            elif choice == "4":
                time.sleep(3)
                subprocess.Popen(["espeak", "stoping object identification"]).wait()
                time.sleep(3)
                print("stoping object identification ")
                objects.stop_object_detection()
                get_first_choice()
                break

            elif choice == "5":
                time.sleep(3)
                subprocess.Popen(["espeak", "starting obstacle detection in the back"]).wait()
                time.sleep(3)
                print("starting obstacle detection in the back")
                obstaclebehinddemo.start_obstacle_behind()
                get_first_choice()
                break

            elif choice == "6":
                time.sleep(3)
                subprocess.Popen(["espeak", "stoping obstacle detection in the back"]).wait()
                time.sleep(3)
                print("stoping obstacle detection in the back")
                obstaclebehinddemo.stop_obstacle_behind()
                get_first_choice()
                break

            elif choice == "7":
                time.sleep(3)
                subprocess.Popen(["espeak", "starting facial recognition"]).wait()
                time.sleep(3)
                print("starting facial recognition")
                facialr.start_facial_recognition()
                get_first_choice()
                break

            elif choice == "8":
                time.sleep(3)
                subprocess.Popen(["espeak", "stoping facial recognition"]).wait()
                time.sleep(3)
                print("stoping facial recognition")
                facialr.stop_facial_recognition()
                get_first_choice()
                break

            elif choice == "*":
                print("Go back to menu")
                time.sleep(3)
                subprocess.Popen(["espeak", "Going back to menu"]).wait()
                time.sleep(3)
                menu()
                break

            elif choice == "#":
                time.sleep(3)
                subprocess.Popen(["espeak", "Turning off  the smart wearable assistant"])
                time.sleep(3)
                sys.exit()
                print("starting facial recognition ")
                menu()
                break

            else:
                menu()
                choice = ""
                break

    return choice


def menu():
    subprocess.Popen(["espeak", "MENU."]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 1 to detect obstacles in the front"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 2  to stop detecting obstacles in the front"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 3  to start  object  identification"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 4  to stop  object  identification"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 5  to start detecting  obstacles in the back"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 6  to stop detecting  obstacles  in the back"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 7  to start facial recognition"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press 8  to  stop facial recognition"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press #  to turn off the smart wearable assistant"]).wait()
    time.sleep(3)
    subprocess.Popen(["espeak", " Press star to go back to menu"]).wait()
    time.sleep(3)
    get_first_choice()


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        print(characters[0])
    if GPIO.input(C2) == 1:
        print(characters[1])
    if GPIO.input(C3) == 1:
        print(characters[2])
    if GPIO.input(C4) == 1:
        print(characters[3])
    GPIO.output(line, GPIO.LOW)


try:
    menu()
    while True:
        # call the readLine function for each row of the keypad
        readLine(L1, ["1", "2", "3", "A"])
        readLine(L2, ["4", "5", "6", "B"])
        readLine(L3, ["7", "8", "9", "C"])
        readLine(L4, ["*", "0", "#", "D"])
        time.sleep(0.1)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nApplication stopped!")
