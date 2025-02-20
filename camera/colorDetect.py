import numpy as np
from matplotlib import pyplot as plt
import cv2
import multiprocessing as mp

COLORS = {
    "red" : 0,
    "yellow" : 60,
    "green" : 120,
    "cyan" : 180,
    "blue" : 240,
    "purple" : 300,
    "red1" : 360,
}

SAT_THRESH = 0.5
VAL_THRESH = 0.3

def getColor(image:np.ndarray) -> str:
    '''
    `image` is an image

    returns the stoplight-color for the center of an image, None if desaturated/dark
    '''

    w = image.shape[0]
    h = image.shape[1]

    cv2.rectangle( image, (int(0.4*h) , int(0.4*w)), (int(0.6*h) , int(0.6*w)), (0,255,0) )
    middle = image[ int(0.4*w):int(0.6*w), int(0.4*h):int(0.6*h) ]

    # ok so average middle
    n = middle[:,:,0].size * 255
    r = float(middle[:,:,0].sum()) / n
    g = float(middle[:,:,1].sum()) / n
    b = float(middle[:,:,2].sum()) / n

    # now get hue
    hue = 0
    if (max(r,g,b) == r): 
        hue = float(g-b)/(max(r,g,b)-min(r,b,g))
    elif (max(r,g,b) == g): 
        hue = 2.0 + float(b-r)/(max(r,g,b)-min(r,b,g))
    else: 
        hue = 4.0 + float(r-g)/(max(r,g,b)-min(r,b,g))


    sat = (max(r,g,b)-min(r,g,b))/max(r,g,b)

    if (sat < SAT_THRESH or max(r,g,b) < VAL_THRESH): return None
    hue *= 60

    # just get the closest named color
    closest_color = "red"
    for color in COLORS:
        if abs(COLORS[color]-hue) < abs(COLORS[closest_color]-hue): closest_color = color
    if closest_color == "red1": closest_color = "red"
    
    img = img[:,:,::-1]

    plt.imshow(img,interpolation="bicubic")
    plt.xticks([]); plt.yticks([])
    plt.show()

    if closest_color in ["red","yellow","green"]: return closest_color
    return None