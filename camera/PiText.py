import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt

#pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"
def readText(img:np.array) -> str:
    '''Reads text from the biggest object in the image'''
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(18,18))
    
    edges = cv2.Canny(cv2.GaussianBlur(img,[3,3],sigmaX=0.1,sigmaY=0.1),100,100)
    dilation = cv2.dilate(edges,rect_kernel,iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    plt.imshow(img,interpolation="bicubic")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    plt.imshow(edges,interpolation="bicubic")
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    plt.imshow(edges,interpolation="bicubic")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    #plt.imshow(contours,interpolation="bicubic")
    #plt.xticks([]); plt.yticks([])

    gooderContours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)

        rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        gooderContours.append((w*h, x, y, w, h))

    gooderContours.sort()

    _, x, y, w, h = gooderContours[-1]
    a = pytesseract.image_to_string(img[y:y+h,x:x+w],lang='eng',config="--psm 10")

    return a
