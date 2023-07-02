import RPi.GPIO as GPIO
import subprocess
import obstacle 
import face
import sys
import time
 
# Set up the GPIO pins and keypad configuration
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

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
        
def get_first_choice():
    print("entering choice")
    choice = ""
    while True:
        choice = readChoice(L1, ["1", "2", "3", "A"], choice)
        choice = readChoice(L2, ["4", "5", "6", "B"], choice)
        choice = readChoice(L3, ["7", "8", "9", "C"], choice)
        choice = readChoice(L4, ["*", "0", "#", "D"], choice)    
        if len(choice) == 1:
            if choice == "1":
                print("Starting obstacle detection...")
                obstacle.start_obstacle_detection()
                menu()
                break
            elif choice == "2":
                print("Stopping obstacle detection and facial recognition...")
                obstacle.stop_obstacle_detection()
                face.stop_facial_recognition()
                menu()
                break
            elif choice == "3":
                print("Starting facial recognition...")
                face.start_facial_recognition()
                menu()
                break
            elif choice == "*":
                subprocess.Popen(["python", "/home/bse3/Desktop/Project/menutest.py"])
                break
            else:
                menu()
                choice = ""
                break
    return choice

def menu():
    subprocess.Popen(["espeak", "MENU."])
    time.sleep(1)
    subprocess.Popen(["espeak", "1. Start obstacle detection."])
    time.sleep(1)
    subprocess.Popen(["espeak", "2. Stop obstacle detection and facial recognition."])
    time.sleep(1)
    subprocess.Popen(["espeak", "3. Start facial recognition."])
    time.sleep(1)
    subprocess.Popen(["espeak", "*. Run menu.py."])
    time.sleep(1)
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
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)
        time.sleep(2)
except KeyboardInterrupt:
    print("\nApplication stopped!")
finally:
    GPIO.cleanup()
