# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
gpio = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio, GPIO.OUT)
GPIO.output(gpio, GPIO.LOW)

# Set GPIO Pins
GPIO_TRIGGER = 17
GPIO_ECHO = 27

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

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

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist < 100:
                print("Intruder detected")
                # Activate vibration here
                GPIO.output(gpio, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(gpio, GPIO.LOW)
                
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
