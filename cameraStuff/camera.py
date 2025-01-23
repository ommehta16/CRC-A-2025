from picamzero import Camera
from time import sleep

cam = Camera()
cam.start_preview() #starts camera preview

cam.start_preview()
cam.take_photo(f"{home_dir}/Desktop/piImageTest1.jpg") #save the image to your desktop
cam.stop_preview()
