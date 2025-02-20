import cv2
import time
from matplotlib import pyplot as plt
import colorDetect


# import TestCam as camera
# import TestText as ocr
# ^^ comment out if you're on pi

# 
import PiCam as camera
import PiText as ocr
# ^^ comment out if you're not on pi

def main():
    img = camera.getFrame()
    
    # cv2.imwrite("derk.jpg",img)
    #img = cv2.imread(f"derk.jpg")

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    rn = time.time()
    print("TEXT:",ocr.readText(img))
    print(f"\nTook {time.time()-rn}s")

    print("COLOR:", colorDetect.getColor(img))
    img = img[:,:,::-1]

    plt.imshow(img,interpolation="bicubic")
    plt.xticks([]); plt.yticks([])
    plt.show()

if __name__ == "__main__": main()
