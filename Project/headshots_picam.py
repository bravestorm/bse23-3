import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray

# List of person names
people = ['David', 'Gabula']

# Number of photos to capture for each person
num_photos = 10

# Initialize the PiCamera
cam = PiCamera()
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))

# Iterate over each person
for person in people:
    print("Capturing photos for", person)
    
    # Create a subfolder for the person's images
    folder_path = "dataset/" + person
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    img_counter = 0
    
    while img_counter < num_photos:
        for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            cv2.imshow("Press Space to take a photo", image)
            rawCapture.truncate(0)
    
            k = cv2.waitKey(1)
            rawCapture.truncate(0)
            if k%256 == 27: # ESC pressed
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = folder_path + "/image_{}.jpg".format(img_counter)
                cv2.imwrite(img_name, image)
                print("{} written!".format(img_name))
                img_counter += 1
                
        if k%256 == 27:
            print("Escape hit, closing...")
            break

cv2.destroyAllWindows()
