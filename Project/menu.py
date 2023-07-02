# import required libraries
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
    print("entering choice")
    choice = ""
    while True:
        choice = readChoice(L1, ["1", "2", "3", "A"], choice)
        choice = readChoice(L2, ["4", "5", "6", "B"], choice)
        choice = readChoice(L3, ["7", "8", "9", "C"], choice)
        choice = readChoice(L4, ["*", "0", "#", "D"], choice)    
        if len(choice) == 1:
            if choice == "1":
                subprocess.Popen(["espeak", "starting obstacle detection in the front"])
                print("starting obstacle detection in the front")
                #vibrate.vibrate()
                obstaclefrontdemo.start_obstacle_front() 
                menu()   
                break;
            elif choice == "2":
                subprocess.Popen(["espeak", "stoping obstacle detection in the front"])
                print("stoping obstacle detection in the front")
                #vibrate.vibrate()
                obstaclefrontdemo.stop_obstacle_front() 
                
                menu()
                break;
            elif choice == "3":
                subprocess.Popen(["espeak", "starting object identification"])
                print("starting object identification ")
                #vibrate.vibrate()
                objects.start_object_detection() 
                #face.start_facial_recognition()
                
                menu()
                break;
                    
            elif choice == "4":
                subprocess.Popen(["espeak", "stoping object identification"])
                print("stoping object identification ")
                #vibrate.vibrate()
                objects.stop_object_detection() 
                
                menu()
                break;
                  
            elif choice == "5":
                subprocess.Popen(["espeak", "starting obstacle detection in the front"])
                print("starting obstacle detection in the back")
                obstaclebehinddemo.start_obstacle_behind()
                #vibrate.vibrate()
                 
                
                menu()
                break;      
                  
            elif choice == "6":
                subprocess.Popen(["espeak", "stoping obstacle detection in the front"])
                print("stoping obstacle detection in the back")
                #print("stoping object detection ")
                #vibrate.vibrate()
                obstaclebehinddemo.stop_obstacle_behind()
                  
                #objects.stop_object_detection()
                menu()
                break;      
                  
            elif choice == "7":
                subprocess.Popen(["espeak", "starting facial recognition"])
                print("starting facial recognition")
                #print("stoping object detection ")
                #vibrate.vibrate()
                facialr.start_facial_recognition()
                #obstaclefrontdemo.stop_obstacle_front() 
                #objects.stop_object_detection()
                
                menu()
                break;      
            
            elif choice == "8":
                subprocess.Popen(["espeak", "stoping facial  recognition"])
                print("stoping facial recognition")
                #print("stoping object detection ")
                facialr.stop_facial_recognition()
                #vibrate.vibrate()
                #obstaclebehinddemo.start_obstacle_front()  
                #objects.stop_object_detection()
                menu()
                break;
                 
            elif choice == "9":
                print("stoping the behind detection sensor")
                #print("stoping object detection ")
                #vibrate.vibrate()
                obstaclebehinddemo.stop_obstacle_behind()  
                #objects.stop_object_detection()
                print("stopped")
                menu()
                break; 
                    
            elif choice == "#":
                subprocess.Popen(["espeak", "shuting down the smart wearable assistant"])
                sys.exit()
                
                print("starting facial recognition ")
                #vibrate.vibrate()
                 
                #face.start_facial_recognition()
                menu()
                break;     
            else:
                menu()
                choice = ""
                break;
    return choice



def menu():
    subprocess.Popen(["espeak", "MENU."])
    time.sleep(3)
    subprocess.Popen(["espeak",  " Press 1 to detect obstacles in the front"])
    time.sleep(3)
    subprocess.Popen(["espeak",  " Press 2  to stop detecting obstacles in the front"])
    time.sleep(3)
    subprocess.Popen(["espeak",   " Press 3  to start  object  identification"])
    time.sleep(3)
    subprocess.Popen(["espeak",   " Press 4  to stop  object  identification"])
    time.sleep(3)
    subprocess.Popen(["espeak",   " Press 5  to start detecting  obstacles in the back"])
    time.sleep(3)
    subprocess.Popen(["espeak",  " Press 6  to stop detecting  obstacles  in the back"])
    time.sleep(3)
    subprocess.Popen(["espeak",   " Press 7  to start facial recognition"])
    time.sleep(3)
    subprocess.Popen(["espeak",   " Press 8  to  stop facial recognition"])
    time.sleep(3)
    subprocess.Popen(["espeak",   " Press #  to turn off the smart wearable assistant"])
    time.sleep(3)
    get_first_choice()
    
def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
    if(GPIO.input(C2) == 1):
        print(characters[1])
    if(GPIO.input(C3) == 1):
        print(characters[2])
    if(GPIO.input(C4) == 1):
        print(characters[3])        
    GPIO.output(line, GPIO.LOW)

    
try:
    menu()
    while True:
        # call the readLine function for each row of the keypad
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\nApplication stopped!")    

 
