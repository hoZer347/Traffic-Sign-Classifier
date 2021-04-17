# Main

import cv2
import numpy as np
import os

CASCADE_FOLDER = "../cascades"

def loadCascades():
    cascades = dict()
    for folder in os.listdir(CASCADE_FOLDER):
        if not "cascade.xml" in os.listdir(f"{CASCADE_FOLDER}\\{folder}"):
            continue
        cascade = cv2.CascadeClassifier()
        if not cascade.load(f"{CASCADE_FOLDER}\\{folder}\\cascade.xml"):
            print("Failed to load cascade classifier")
            continue
        cascades[folder] = cascade
    return cascades

def applyHaarCascade(frame, cascade):
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.equalizeHist(gray)
    signs = cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=20, flags=cv2.CASCADE_SCALE_IMAGE)
    return signs

def main():
    cascades = loadCascades()

    # Change this img to whatever image name
    img = cv2.imread("images.jfif")

    signs = []
    for cascade in cascades:
        print(len(signs))
        new_signs = applyHaarCascade(img, cascades[cascade])
        for sign in new_signs:
            signs.append(sign)

    for (x,y,w,h) in signs:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        signROI = img[y:y+h,x:x+w]
    
    cv2.imshow("img", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
