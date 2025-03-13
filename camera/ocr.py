import numpy as np
from matplotlib import pyplot as plt
import cv2

DILATE_AMT = 25

def readText(img:np.array) -> str:
    dilation, text_aabbs = split_img(img)

    '''
    OK SO WHAT IM THINKING RN

    we have it chopped up into aabbs (axis aligned bounding box)

    aabbs is normally bad, but here is good
    
    ok how about this

    take whats in the aabbs

    and train neural net based on that

    HOW?

    

    '''
    
    return ""
    
def split_img(img:np.array) -> tuple[np.array, list[tuple]]:
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(DILATE_AMT,DILATE_AMT))
    
    edges = cv2.Canny(cv2.GaussianBlur(img,[3,3],sigmaX=0.1,sigmaY=0.1),100,100)
    dilation = cv2.dilate(edges,rect_kernel,iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    plt.imshow(dilation,interpolation="bicubic")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    # cv2.drawContours(img,contours,-1,(255,0,0),2)
    text_aabbs = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text_aabbs.append((x, y, w, h))
    
    return dilation, text_aabbs