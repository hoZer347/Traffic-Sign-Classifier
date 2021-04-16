# Main

import cv2
import numpy as np
import os

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

CASCADE_DIR = "../training/Images/00000/_data/cascade.xml"

def detectAndDisplay(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    signs = cascade.detectMultiScale(frame, scaleFactor=1.4, minNeighbors=4, flags=cv2.CASCADE_SCALE_IMAGE)
    print(signs)
    for (x,y,w,h) in signs:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        signROI = frame[y:y+h,x:x+w]
    cv2.imshow("Image", frame)

def main():
    cascade = cv2.CascadeClassifier()
    if not cascade.load(CASCADE_DIR):
        print("Failed to load cascade classifier")
        return

    # Change this img to whatever image name
    img = cv2.imread("notrucks.png")
    detectAndDisplay(img, cascade)

    #Code for video stream below...
    # camera = cv2.VideoCapture(0)

    # cascade_0 = cv2.CascadeClassifier()
    # if not cascade_0.load(CASCADE_0_DIR):
    #     print("Failed to load cascade classifier")
    #     return

    # while True:
    #     ret, frame = camera.read()
    #     if frame is None:
    #         print("Error: No frame read from video stream.")
    #         break
    #     detectAndDisplay(frame, cascade_0)
    #     # cv2.imshow('Camera Feed', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # camera.release()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
