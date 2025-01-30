import numpy as np
import time
import os

import cv2

cam = cv2.VideoCapture(0)

def getFrame() -> np.ndarray:
    res, img = cam.read()

    rn = time.time()
    while True:
        if res or time.time()-rn > 2: break

        res, img = cam.read()
    if not res:
        raise PermissionError("Permission to use camera denied :(")
    return img

