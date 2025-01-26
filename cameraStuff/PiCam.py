from picamera2 import Picamera2

from picamzero import Camera
import numpy as np
from time import sleep
import os

def getFrame() -> np.ndarray:
    # Derek pls implement this

    # It just has to take a picture and save it to some inbuilt data type (NOT a file pls)
    # return that datatype once your done
    
    # thanks :)
    
    return np.zeros([1,1])
    




home_dir = os.environ['HOME'] #set the location of your home directory

cam = Camera()
cam.start_preview() #starts camera preview

"""
#VIDEO
cam.start_preview()
cam.record_video(f"{home_dir}/Desktop/new_video.mp4", duration=5)
cam.stop_preview()
"""

#RAPID PICTURES test 
for i in range(3): #use while true loop later
    cam.take_photo(f"{home_dir}/Desktop/new_image"+str(i)+".jpg") #save the image to your desktop
    print("Captured Image "+str(i))
    sleep(0.5) #seconds