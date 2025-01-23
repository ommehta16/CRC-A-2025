import cv2
import time
from matplotlib import pyplot as plt


def main():
    cam = cv2.VideoCapture(0)
   
    res,img = cam.read()
    for _ in range(1000):
        if res: break
        time.sleep(0.01)
        res,img = cam.read()
    print(res)
    img = img[:,:,::-1]
    plt.imshow(img,interpolation="bicubic")
    plt.xticks([]); plt.yticks([])
    plt.show()

    # do image processings
if __name__ == "__main__": main()