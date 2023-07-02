import RPi.GPIO as GPIO
import time
import subprocess
import threading

GPIO.setmode(GPIO.BCM)


global obstacle_detected1, obstacle_detected2
def obstacle_detection():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    buzzer_pin = 22
    vibration_pin1 = 22
    vibration_pin2 = 23
    TRIG1 = 5
    ECHO1 = 6
    TRIG2 = 17
    ECHO2 = 27

    GPIO.setup(vibration_pin1, GPIO.OUT)
    GPIO.setup(vibration_pin2, GPIO.OUT)
    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)
    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(ECHO2, GPIO.IN)

    GPIO.output(TRIG1, False)
    GPIO.output(TRIG2, False)
    print("Initializing sensors")
    time.sleep(2)


    def vibrate(vibration_pin):
        GPIO.output(vibration_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(vibration_pin, GPIO.LOW)


    def activate_buzzer():
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.2)


    def measure_distance(trig_pin, echo_pin):
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance


    obstacle_detected1 = False
    obstacle_detected2 = False
    stop_obstacle_detection = threading.Event()


    try:
        while not stop_event.is_set():
            while True:
                if not obstacle_detected1:
                    distance1 = measure_distance(TRIG1, ECHO1)
                    print("Distance from Sensor 1:", distance1, "cm")

                    if distance1 <= 200:
                        obstacle_detected1 = True
                        activate_buzzer()
                        vibrate(vibration_pin1)
                        vibrate(vibration_pin2)
                        direction = "front"
                        feedback = f"Obstacle detected {distance1} centimeters ahead in the {direction} direction by Sensor 1"
                        print(feedback)
                        subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])

                        direction = "try right or left until vibrations stop"
                        print(feedback)
                        subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])


                if not obstacle_detected2:
                    distance2 = measure_distance(TRIG2, ECHO2)
                    print("Distance from Sensor 2:", distance2, "cm")
                    subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])


                    if distance2 <= 200:
                        obstacle_detected2 = True
                        activate_buzzer()
                        vibrate(vibration_pin2)
                        vibrate(vibration_pin1)
                        direction = "front"
                        feedback = f"Obstacle detected {distance2} centimeters ahead in the {direction} direction by Sensor 2"
                        print(feedback)
                        subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])
                        direction = "try right or left until vibrations stop"
                        print(feedback)
                        subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])

                while obstacle_detected1:
                    distance1 = measure_distance(TRIG1, ECHO1)
                    print("Distance from Sensor 1:", distance1, "cm")
                    feedback = f"Obstacle detected {distance1} centimeters ahead in the {direction} direction by Sensor 1"
                    print(feedback)
                    subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])
                    direction = "try right or left until vibrations stop"
                    print(feedback)
                    subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])

                    if distance1 > 200:
                        obstacle_detected1 = False
                        print("You have turned away from the obstacle detected by Sensor 1")
                        subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])
                        print("now try turning back and continue moving")
                        subprocess.call(["espeak", "-s", "150", "-ven-us", feedback])
                        break

                    activate_buzzer()
                    vibrate(vibration_pin1)
                    vibrate(vibration_pin2)

                while obstacle_detected2:
                    distance2 = measure_distance(TRIG2, ECHO2)
                    print("Distance from Sensor 2:", distance2, "cm")
                    feedback = f"Obstacle detected {distance2} centimeters ahead in the {direction} direction by Sensor 2"
                    print(feedback)
                    direction = "try right or left until vibrations stop"
                    print(feedback)

                    if distance2 > 200:
                        obstacle_detected2 = False
                        print("You have turned away from the obstacle detected by Sensor 2")
                        print("now try turning back and continue moving")
                        break

                    activate_buzzer()
                    vibrate(vibration_pin2)
                    vibrate(vibration_pin1)

                time.sleep(0.5)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.output(vibration_pin1, GPIO.LOW)
        GPIO.output(vibration_pin2, GPIO.LOW)
        GPIO.cleanup()

# Create a threading.Event object to signal the process to stop
stop_event = threading.Event()

# Function to start the obstacle detection process in a separate thread
def start_obstacle_detection():
    # Reset the stop event flag to allow starting the process again
    stop_event.clear()
    # Create a new thread and start the obstacle detection function
    obstacle_detection_thread = threading.Thread(target=obstacle_detection)
    obstacle_detection_thread.start()

# Function to stop the obstacle detection process
def stop_obstacle_detection():
    # Set the stop event to signal the obstacle detection process to stop
    stop_event.set()
