# Soil moisture test
import time
import RPi.GPIO as GPIO
import os
import numpy as np
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np

# Define parameters of ADC 
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs) # create an MCP3008 object

# Define analog input channels and GPIO pins for respective sensors
channel_soil = AnalogIn(mcp, MCP.P1)   # soil_input

# Calibration period
p = 5 # seconds

data_soil = []

# Collect data for one minute
# First for soil moisture sensor in dry air  --> humidity = 0%
# Second for soil moisture sensor in water   --> humidity = 100%
for i in range(p):
    print('ADC Soil Voltage = ' + str(channel_soil.voltage) + 'V')
    data_soil.append(channel_soil.voltage)  # append soil voltage value
    if i != (p/2)-1:
        time.sleep(1)   # sleep for 1 second
    else:
        time.sleep(20)  # sleep for 20 seconds between dry and wet measurements

data_soil = np.array(data_soil)

# Then take the mean and record below
print('Soil voltage avg = ', np.mean(data_soil))

# mean of dry air voltage: 2.225546654459449
# mean of water voltage: 0.9987164110780499