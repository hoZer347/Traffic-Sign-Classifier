# Main

import cv2

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

def main():
    img = cv2.imread("../stop_sign.jpg")
    cv2.imshow("stop sign", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()