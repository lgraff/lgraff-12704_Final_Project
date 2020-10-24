# Light Calibration

# Import libraries
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
import matplotlib.pyplot as plt

# Define parameters of ADC 
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

mcp = MCP.MCP3008(spi, cs) # create an MCP3008 object

# Define analog input channels and GPIO pins for respective sensors
channel_light = AnalogIn(mcp, MCP.P0)  # light input

# Calibration period
p = 20 # seconds

data_light = [] 

# Collect data for 20 seconds for different lighting conditions
# Then manually record the results in the subsequent "light_results" array
for i in range(p):
    print('ADC light Voltage = ' + str(channel_light.voltage) + 'V')
    data_light.append(channel_light.voltage)  # append light voltage value
    time.sleep(1)

data_light = np.array(data_light)
avg_light = np.mean(data_light)
print()
print('avg light = ', avg_light)

# [voltage,lux]
light_results = np.array([[1.10,356],
                          [1.236,445],
                          [2.092,136],
                          [0.9836,572],
                          [1.27,717],
                          [0.912,1153],
                          [0.963,959],
                          [1.959,218],
                          [2.16,107],
                          [1.397,281],
                          [1.698,173],
                          [0.731,1443],
                          [0.607,1806],
                          [0.524,2314]])

# Plot results, first on linear scale then on log-log scale
def plot_light(scale):
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(light_results[:,1], light_results[:,0])
    ax.set_xscale(scale)  
    ax.set_yscale(scale)  
    ax.set_title('Light Sensor calibration')
    ax.set_xlabel('Lux')
    ax.set_ylabel('Voltage')
    #ax.set_xlim([100,2500])
    #ax.set_ylim([0.1,4])
    fig.show()

plot_light('linear')
plot_light('log')
           
# Then fit a least squares lines to the log results
z = np.polyfit(np.log10(light_results[:,1]), np.log10(light_results[:,0]),1)