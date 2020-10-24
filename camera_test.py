from picamera import PiCamera
import time
from PIL import Image

camera = PiCamera() 
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
camera.brightness = 60
camera.contrast = 60

# Capture 3 consistent images
for i in range(4,7):
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
    imagepath = '/home/pi/Desktop/basil project prototype/basil_images/image_consistency_test' + str(i) + '.jpg'
    camera.capture(imagepath)
    #imagepath=cwd+'/basil_images/' + 'basil_image' + str(j-1) + '.jpg'
    img = Image.open(imagepath) #'/home/pi/Desktop/basil project prototype/basil_images/basil_image1.jpg')
    # Crop the image
    # source1: https://www.geeksforgeeks.org/python-pil-image-crop-method/
    # source2: https://stackoverflow.com/questions/1076638/trouble-using-python-pil-library-to-crop-and-save-image
    width, height = img.size  # sjze of original image
    left = (1/3)*width  # left starting coordinate of the box to crop 
    top = 0             # top starting coordinate of the box to crop
    width = (1/3)*width # desired cropped image width 
    height = height     # desired cropped image height 
    box = (left, top, left+width, top+height)  # coordinates of box to crop
    img_crop = img.crop(box)  # cropped image
    # Save the cropped image over the original image
    img_crop.save(imagepath)
    
    
    