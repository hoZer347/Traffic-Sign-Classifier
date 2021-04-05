# Main

import cv2
import numpy as np

# - Pre-optimization
# 	- Unkown optimizations (Do after it works)
# 	- Generating neural network
# - Sign detection (there is a sign!)
# 	- Haar Cascade Classifiers
# - Sign registration
# - Feature extraction
# 	- HOG feature detection
# - Recognition
# - Output\

CASCADE_0_DIR = "../training/Images/00000/_data/cascade.xml"
# CASCADE_0_DIR = "test.xml"

def detectAndDisplay(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    #-- Detect faces
    faces = cascade.detectMultiScale(gray, 1.4, 3, flags=cv2.CASCADE_SCALE_IMAGE, minSize=(40, 40))
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        faceROI = gray[y:y+h,x:x+w]
    cv2.imshow('Capture - Face detection', frame)

def main():
    # img = cv2.imread("../stop_sign.jpg")
    # cv2.imshow("stop sign", img)
    camera = cv2.VideoCapture(0)

    cascade_0 = cv2.CascadeClassifier()
    if not cascade_0.load(CASCADE_0_DIR):
        print("Failed to load cascade classifier")
        return

    while True:
        ret, frame = camera.read()
        if frame is None:
            print("Error: No frame read from video stream.")
            break
        detectAndDisplay(frame, cascade_0)
        # cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
