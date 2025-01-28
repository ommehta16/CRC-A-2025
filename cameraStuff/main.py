import cv2
import time
from matplotlib import pyplot as plt

import TestCam as camera
import TestText as ocr
# ^^ comment out if you're on pi

# 
# import PiCam as camera
# import PiText as ocr
# ^^ comment out if you're not on pi

def main():
    img = cv2.imread("sample.jpg")
    
    rn = time.time()
    print(ocr.readText(img))
    print(f"{time.time()-rn}s")

    img = img[:,:,::-1]
    plt.imshow(img,interpolation="bicubic")
    plt.xticks([]); plt.yticks([])
    plt.show()

if __name__ == "__main__": main()