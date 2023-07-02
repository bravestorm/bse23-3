import RPi.GPIO as GPIO
import time
import threading
import subprocess

def obstaclefront():
    # GPIO Mode (BOARD / BCM)
    global stop_thread
    gpio = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.LOW)

    # Set GPIO Pins
    GPIO_TRIGGER = 5
    GPIO_ECHO = 6

    # Set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Flag to control obstacle detection thread
    stop_thread = False

    def distance():
        # Set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # Set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # Save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        # Save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        # Time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # Multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

    while not stop_thread:
        dist = distance()
        if dist < 100:
            print("obstacle detected")
            subprocess.Popen(["espeak", "obstacle detected turn left or right"]).wait()
            time.sleep(3.5)
            # Activate vibration here
            GPIO.output(gpio, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(gpio, GPIO.LOW)
        print("Measured Distance = %.1f cm" % dist)
        time.sleep(1)

def start_obstacle_front():
    global stop_thread
    stop_thread = False
    thread = threading.Thread(target=obstaclefront)
    thread.start()

def stop_obstacle_front():
    global stop_thread
    stop_thread = True

if __name__ == '__main__':
    try:
        start_obstacle_front()
        while True:
            # Main program loop
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        stop_obstacle_front()
        GPIO.cleanup()
