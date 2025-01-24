from picamzero import Camera
from time import sleep
import os

home_dir = os.environ['HOME'] #set the location of your home directory

cam = Camera()
cam.start_preview() #starts camera preview

#RAPID PICTURES test 

#settings
pictureDelayInterval = 0.1 #IN SECONDS 
numberPicturesTaken = 3 #take 3 pictures

#take a bucnh of pictures:
for i in range(numberPicturesTaken): #use while true loop later
    cam.take_photo(f"{home_dir}/Desktop/new_image"+str(i)+".jpg") #save the image to your desktop
    print("Captured Image: "+str(i))
    sleep(pictureDelayInterval) #seconds

cam.stop_preview()