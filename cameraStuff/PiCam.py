from picamera2 import Picamera2

from picamzero import Camera
import numpy as np
from time import sleep
import os

from PIL import Image #python imaging library
import oi #file input stuff



#home_dir = os.environ['HOME'] #set the location of your home directory

cam = Camera()
cam.start_preview() #starts camera preview

#RAPID PICTURES test 

#settings
pictureDelayInterval = 0.1 #IN SECONDS 
numberPicturesTaken = 3 #take 3 pictures

#list of images
imageList = []

#take a bucnh of pictures:
for i in range(numberPicturesTaken): #use while true loop later

    #cam.take_photo(f"{home_dir}/Desktop/new_image"+str(i)+".jpg") #save the image to your desktop
    
    memoryStream = io.BytesIO()
    cam.capture(memoryStream, format = 'jpeg')
    memoryStream.seek(0)

    #convert image to np array
    image = Image.open(stream)
    imageArray = np.array(image) #converts image to array

    imageList.append(imageArray)
    
    print("Captured Image: "+str(i))
    sleep(pictureDelayInterval) #seconds

cam.stop_preview()
cam.close()