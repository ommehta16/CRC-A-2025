from picamzero import Camera
from time import sleep
import os

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
    cam.take_photo("new_image"+str(i)+".jpg") #save the image to your desktop
    print("Captured Image "+str(i))
    sleep(0.5) #seconds