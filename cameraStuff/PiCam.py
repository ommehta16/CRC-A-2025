from picamera2 import Picamera2

from picamzero import Camera
import numpy as np
from time import sleep
import os

from PIL import Image #python imaging library
import oi #file input stuff

def getFrame() -> np.ndarray:
    
    #home_dir = os.environ['HOME'] #set the location of your home directory

    cam = Camera()
    cam.start_preview() #starts camera preview


    #cam.take_photo(f"{home_dir}/Desktop/new_image"+str(i)+".jpg") #save the image to your desktop
        
    memoryStream = io.BytesIO()
    cam.capture(memoryStream, format = 'jpeg')
    memoryStream.seek(0)

    #convert image to np array
    image = Image.open(memoryStream)
    imageArray = np.array(image) #converts image to array

    #print("Captured Image: "+str(i))

    return imageArray
