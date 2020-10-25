# 12-740 Final Project
# Hi-Tech Basil
## First Progress Report
### Current Progress
- Set up the circuit for all sensors and confirmed that they are taking measurements when exposed to physical stimuli. This includes the temperature/humidity sensor, light sensor, and soil moisture sensor. The soil moisture sensor was something we purchased externally. We also tested that this circuit works specifically in the environment of the basil plant subject we're using.
- Wrote basic Python code to record the measurements of each sensor.
- Connected a camera to the circuit and wrote code to take repeated photos after a time interval
- Thought about which metrics would be appropriate to use as a measure of plant changes over time. One option is to output a before vs. after picture of the plant for each time interval, letting the user define the relative growth. This is our first goal. Time permitting, two possible quantifiable options are: 1) plant height, which may be measured through height tick marks drawn behind the plant (and seen in the image), and 2) the color intensity of green pixels in the image.
- Investigated the PiCamera module and basic image processing in Python to understand the feasibility of the last two quantifiable options. The PiCamera module will also us to capture: 1) a still image at given time intervals, and 2) the raw RGB data of each pixel stored as a NumPy array. It seems we would want to store both of these. We have already shown that we can capture a still image, but haven't yet completed the second part in practice.

### Problems Encountered
- Setting up the physical space; how to ensure that the sensors are directly next to the plant while also ensuring that the camera is far enough to capture the image of the full plant? It would also be helpful to have the photo of the plant be taken against a relatively blank backdrop.
- Figuring out how to find plant height from the image; we thought about the tick marks method described above, but we're unclear how to extract this dynamic value through code
- Figuring out how to cleanly extract the green color intensity of the image; since we are only interested in the plant, how we can ensure that we do not pick up the noise of the green pixels in the background?
- Deciding which data to keep; do we want to keep all sensor values recorded at the shorter intervals, or just the average of the 8 hour period?

### Future Plan
- Determine how to convert the output voltage values of the soil moisture sensor to a soil moisture percentage. This link (https://www.switchdoc.com/2020/06/tutorial-capacitive-moisture-sensor-grove/) should be helpful.
- Learn more about basic image processing to see what data we can extract from our images. 
- Create a database to store the average temperature, humidity, light, and soil moisture values of the past 6 or 8 hours, along with a picture of the plant at that time step and possibly a measure of growth in the past 6 or 8 hours. This will require us to sense temp/humidity/light/moisture at relatively short intervals, take the average of the time interval, and then record the values. Each row of the database will represent a different time interval.
- Determine how to connect everything to an IoT app and decide what to display to users. We imagine an app that displays a row of the database corresponding to each time interval i.e. the user can see avg temp/humidity/light/moisture, along with a before vs. after photo of the plant.
