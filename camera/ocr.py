import numpy as np
from matplotlib import pyplot as plt
import cv2

def readText(img:np.array) -> str:
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(18,18))
    
    
    edges = cv2.Canny(cv2.GaussianBlur(img,[3,3],sigmaX=0.1,sigmaY=0.1),100,100)
    dilation = cv2.dilate(edges,rect_kernel,iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    # plt.imshow(img,interpolation="bicubic")
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()

    # plt.imshow(edges,interpolation="bicubic")
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()

    gooderContours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        gooderContours.append((w*h, x, y, w, h))


    return ""