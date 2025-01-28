import cv2
import numpy as np
import pytesseract

def readText(img:np.array) -> str | None:
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(18,18))
    dilation = cv2.dilate(thresh,rect_kernel,iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    out = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        tmp = pytesseract.image_to_string(img[x:x+w,y:y+h])

        if tmp is None: continue
        out = str(tmp[0]).lower()
    return out