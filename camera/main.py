import cv2
import time
from matplotlib import pyplot as plt
import colorDetect
import ocr


import TestCam as camera
# import TestText as ocr
# ^^ comment out if you're on pi

# 
# import PiCam as camera
# import PiText as ocr
# ^^ comment out if you're not on pi

def main():
    #img = cv2.imread("you.png")
    img = camera.getFrame()

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    ocr.readText(img)
    # cv2.imwrite("you.png",img)
    # print("COLOR:", colorDetect.getColor(img))

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    plt.imshow(img,interpolation="bicubic")
    plt.xticks([]); plt.yticks([])
    plt.show()

if __name__ == "__main__": main()
