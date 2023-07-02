import cv2
import subprocess
import threading
 


classNames = []
classFile = "/home/bse3/Desktop/Object_Detection_Files/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/bse3/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/bse3/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

stop_event = threading.Event()

def speak(text):
    subprocess.run(["espeak", text])

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects and confidence >= thres:
                objectInfo.append([box, className, (box[0], box[1], box[0] + box[2], box[1] + box[3])])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                    # Convert the object and location information to speech
                    object_text = "Object: " + className
                    center_x = (box[0] + box[2]) / 2
                    if center_x < img.shape[1] / 2:
                        location_text = "Location: Left side"
                    else:
                        location_text = "Location: Right side"
                    speak(object_text)
                    speak(location_text)

    return img, objectInfo

def object_detection():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while not stop_event.is_set():
        success, img = cap.read()
        result, objectInfo = getObjects(img, 0.7, 0.2)  # Adjust the threshold and NMS values as needed
        cv2.imshow("Output", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

def start_object_detection():
    stop_event.clear()
    object_detection_thread = threading.Thread(target=object_detection)
    object_detection_thread.start()

def stop_object_detection():
    stop_event.set() 
