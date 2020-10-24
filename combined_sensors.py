# Use Raspberry Pi to get temperature/humidity/soil moisture/
# light data from sensors
# Also take a picture and record the image as well as array of
# RGB values; then take average of green intensity

# Import libraries
import time
import dht11
import RPi.GPIO as GPIO
import os
import numpy as np
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from picamera import PiCamera
import picamera.array
from PIL import Image
import numpy as np
import datetime as dt
import paho.mqtt.client as mqtt
from twython import Twython as tw
from auth import ( consumer_key, consumer_secret, access_token, access_token_secret)
twitter = tw( consumer_key, consumer_secret, access_token, access_token_secret)
cwd = os.getcwd() # current working directory

# MQTT client
class Device(mqtt.Client):
    def __init__(self, username, password):
        super(Device, self).__init__()
        self.host = "mqtt.openchirp.io"
        self.port = 8883
        self.keepalive = 300
        self.username = username
        self.password = password
        
        # Set access credential
        self.username_pw_set(username, password) #set username and pass
        self.tls_set('cacert.pem')
        
        # Create a dictionary to save all transducer states
        self.device_state = dict()
        
        # Connect to the Broker, i.e. OpenChirp
        self.connect(self.host, self.port, self.keepalive)
        self.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection Successful")
        else:
            print("Connection Unsucessful, rc code = {}".format(rc))
        # Subscribing in on_connect() means that if we lose the connection and reconnect, the subscriptions will be renewed.
    # Subscribe to all transducers
        self.subscribe("openchirp/device/"+self.username+"/#") 

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload.decode()))
        
    # Change Actuator State based on Commands Issued from OpenChirp
        transducer = msg.topic.split("/")[-1]
        self.device_state[transducer] = msg.payload.decode()

    def on_publish(self, client, userdata, result):
        print("Data published")

username = '5f8b0735004d6e55c61dd4bb' # Use Device ID as Username
password = 'nJX9qZvguY97kPoqoZVzqBh5mdHfrYup' # Use Token as Password

# Instantiate a client for device
smart_basil = Device(username, password)

# Tweeting function
# Source: https://projects.raspberrypi.org/en/projects/getting-started-with-the-twitter-api
def tweet(parameters, imagepath): #list of parameters
    image=open(imagepath, "rb") # show image
    # Then show caption
    line1="Good morning to all! In the last 24 hours, the average values of my parameters were:\n\n"
    line2="Humidity (%): {}\n".format(round(parameters[1],1))
    line3="Temperature (°C): {}\n".format(round(parameters[0],1))
    line4="Soil Moisture (%): {}\n".format(round(parameters[3],1))
    line5="Light Intensity (Lux): {:,}\n".format(int(parameters[2]))  
    line6="Average Green Intensity: {}\n\n".format(round(parameters[4],0))
    line7="This is how I woke up today..."
    response= twitter.upload_media(media=image)
    media_id=[response['media_id']]
    message=line1+line2+line3+line4+line5+line6+line7
    twitter.update_status(status=message, media_ids=media_id)

# Define parameters of ADC 
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs) # create an MCP3008 object
camera=PiCamera() # create camera object

# Set camera parameters to capture consistent images
# source: https://picamera.readthedocs.io/en/release-1.10/recipes1.html

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

# Define analog input channels and GPIO pins for respective sensors
channel_light = AnalogIn(mcp, MCP.P0)  # light input
channel_soil = AnalogIn(mcp, MCP.P1)   # soil_input
temp_sensor = 4  #temp/humidity input


# Main program block
def main():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  instance_th = dht11.DHT11(pin = temp_sensor)  # temp/hum instance
  n = 24*60 # take average every n periods; we will take average every hour
  p = 60 # number of seconds between measurements; we will take measurements every 60 seconds
  
  # Prepare to create database of sensor values and green intensity
  filename="data_all.csv" 
  text=open(filename,"w")
  text.close()
  
  # Name sensors for OpenChirp
  sensor_light = "light_sensor"
  sensor_temp = "temperature"
  sensor_hum = "humidity"
  sensor_soil = "soil_moisture"
    
  # Initialize
  smart_basil.device_state[sensor_light] = 0
  smart_basil.device_state[sensor_temp] = 0
  smart_basil.device_state[sensor_hum] = 0
  smart_basil.device_state[sensor_soil] = 0
 
  # Read for n seconds, taking measurements every minute. At the end of the period, take still photo and tweet
  while True:
    data_nperiods = []
    j=1
    for i in range(n):  
          # Get sensor value 
          result_th = instance_th.read()
          if(result_th.temperature==0 and result_th.humidity==0):
            result_th.humidity=float("NaN")
            result_th.temperature=float("NaN")
          # Add timestamp for camera photo 
          camera.annotate_background = picamera.Color('black')
          camera.annotate_text = dt.datetime.now().strftime('%m/%d/%Y, %H:%M%p')
          
          # Print values for testing purpose
          #print("Time: ", time.ctime())
          #print("Temperature = ",result_th.temperature,"C",
           #     " Humidity = ",result_th.humidity,"%")
          #print('ADC Light Voltage = ' + str(channel_light.voltage) + 'V')
          #print('ADC Soil Voltage = ' + str(channel_soil.voltage) + 'V')
          #print()
           
          # Only capture a photo at the end of the hour-long period
          # These will be stored in a folder called "basil_images"
          if i== n-1:  
              camera.capture(cwd+'/basil_images/' + 'basil_image' + str(j) + '.jpg')
              j+=1
              
          # Add the observations of the sensors to the list of data
          soil_moisture = -81.5661*channel_soil.voltage + 181.4845
          lux = 10**((np.log10(channel_light.voltage) - 1.23)/-0.4327)
          aux=(time.ctime(), result_th.temperature, result_th.humidity,
               lux, soil_moisture)
          data_nperiods.append(aux)
          #data_all.append(aux)
          
          # Publish onto OpenChirp
          smart_basil.publish("openchirp/device/"+username+"/"+sensor_light,
                              payload=lux, qos=0, retain=True)
          smart_basil.publish("openchirp/device/"+username+"/"+sensor_soil,
                              payload=soil_moisture, qos=0, retain=True)
          smart_basil.publish("openchirp/device/"+username+"/"+sensor_temp,
                              payload=result_th.temperature, qos=0, retain=True)
          smart_basil.publish("openchirp/device/"+username+"/"+sensor_hum,
                              payload=result_th.humidity, qos=0, retain=True)
          print('Your data has been published')
          # Update device state
          smart_basil.device_state[sensor_light] = lux
          smart_basil.device_state[sensor_soil] = soil_moisture
          smart_basil.device_state[sensor_temp] = result_th.temperature
          smart_basil.device_state[sensor_hum] = result_th.humidity
          
          time.sleep(p)  # sleep for p seconds
        
    # Image processing
    imagepath=cwd+'/basil_images/' + 'basil_image' + str(j-1) + '.jpg'
    img = Image.open(imagepath) 
    
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
    
    # Find the green intensity of the cropped image
    RGB_array = np.array(img_crop)  # RGB of full image
    green_avg = int(np.mean(RGB_array,axis=(0,1))[1])  # average green of pixels

    # Write observations to the database
    text=open(filename, "a")
    for i,t in enumerate(data_nperiods):
        if i==n-1:
            green = green_avg  
        else:
            green = float("NaN")  # if the row does not represent the end of the period, we have a null value for green intensity b/c no image
        t_all = list(t)
        t_all.append(green)
        t_all=tuple(t_all)
        text.write("{},{},{},{},{},{}\n".format(t_all[0],t_all[1],t_all[2],t_all[3],
                                             t_all[4],t_all[5]))  
    text.close()
    print("Observations have been written to database") 
     
    data_nperiods = np.array(data_nperiods)  # cast data as array
    data_nperiods = data_nperiods[:,1:].astype('float64')
    data_avg = np.nanmean(data_nperiods,axis=0)  # then take the average of the period, to be tweeted

    # Tweet; at the end of 24 hours, tweet the average sensor values + green intensity of the image
    list_avg=list(data_avg)
    list_avg.append(green_avg)
    tweet(list_avg, imagepath)
    print("Your tweet has been published")

  #np.save(cwd + "/basil_avg", np.array(data_avg))
  
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass

