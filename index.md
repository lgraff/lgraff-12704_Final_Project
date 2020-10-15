# 12-740 Final Project
# Hi-Tech Basil

## Introduction
In this project, we describe how to set up a sensing and data broadcasting system for any homegrown plant. The data is captured by the Raspberry Pi and sensors, and made available through twitter, an IoT platform, and a .csv file, for people to use. If enough people do the same, we would then be able to have a very useful database to find the optimal ranges for all the factors that promote growth of plants.
## Motivation
Growing plants indoors requires attention to a variety of environmental factors, including temperature, humidity, light, and soil moisture levels. Regulation of these parameters can be difficult, especially when there is sparse data concerning ideal growing conditions for individual plants. Specifically for the basil herb, a quick online search will reveal several different choices that an individual may make when tuning the ambient environmental factors. Notably, however, most sources are primarily anecdotal; homegrowers have yet to document the environmental conditions and associated growth patterns of their plants over time. To address these needs, we propose Hi-Tech Basil: a tweeting indoor basil plant with an associated database, and IoT capabilities. Analyzing the hourly records of this database, in addition to visualizing photos of the plant included in live daily tweets, may provide home growers with insight that optimizes the growth of their indoor plants.
## Project Sketch
Our setup is described in Figure 1.

**INSERT FIGURE 1 WITH TITLE AND SOURCE**

## Main Goal
To setup a sensing and data broadcasting system for homegrown plants.
## Specific Goals
*	Create a sensing system that measures ambient humidity and temperature, ambient light intensity, soil moisture, and also takes a picture of the plant every day.
*	Create a growth status index that can be automatically extracted from the picture taken.
*	Store the collected data on a .csv file, and automatically tweet a summary of the daily surveyed data.
*	Integrate the setup to an IoT platform.
*	Show feasibility of the creation of a massive database by combining experiments by many individuals.
# Methodology
## Phenomena of Interest
Here, we will establish what exacly are the physical phenomena we are measuring, and why they are of interest. Since all the phenomena here vary very slowly in time, they can all be considered static in nature.

**Soil moisture:** this is basically the amount of water available in the soil. It can be measured as a ratio of volume of water per unit volume of soil, or as a ratio of water mass per unit mass of soil. We opt for the second measure because it is easier to measure, and so the calibration of the soil moisture sensor is easy to do at home. The importance of this variable for plant growth is widely known. Here, I quote a passage from Reference 1:

*“…*

*Importance of Soil Water:*

*-Soil water serves as a solvent and carrier of food nutrients for plant growth*

*-Yield of crop is more often determined by the amount of water available rather than the deficiency of other food nutrients*

*-Soil water acts as a nutrient itself*

*-Soil water regulates soil temperature*

*-Soil forming processes and weathering depend on water*

*-Microorganisms require water for their metabolic activities*

*-Soil water helps in chemical and biological activities of soil*

*-It is a principal constituent of the growing plant*

*-Water is essential for photosynthesis*

*…”*

**Ambient humidity:** roughly defined as the amount of water in the air, relative to the maximum amount of water the air can hold at a given temperature. The strict definition is taken from Reference 2:

*“…*

*The relative humidity (RH) is the ratio of the actual water vapour pressure to the saturation water vapour pressure at the prevailing temperature. For example – if a cubic metre can hold 100ml of water at 20 degrees centigrade (273 K) and it does contain 100ml then it is said to be 100% RH. If the same cubic metre of air at the same temperature only contains 50mls of water then it is described as 50% RH.*

*…”*

The importance of this factor from plant growth is explained in the next passage, taken from Reference 3:

*“…*

*If your grow room humidity is low (dry), it causes the plants to transpire much more rapidly than in a higher humidity environment. When this happens, the leaves become flaccid and begin to wilt, and over a longer period of time the plant will close its stomata, and reduce the flow of water out of the plant. This is very effective at stopping water loss, but unfortunately, it also reduces the intake of CO2. Without an adequate supply of CO2, the cells will begin to die, and the plant will look tired and ill.*

*…”*

**Ambient temperature:** this is just the temperature of the room in which the plant is. This factor affects most plant processes. The next passage is taken from Reference 4:

*“…*

*Temperature influences most plant processes, including photosynthesis, transpiration, respiration, germination, and flowering. As temperature increases (up to a point), photosynthesis, transpiration, and respiration increase.*

*…”*

**Ambient light intensity:** measuring light intensity near the plant will give us the amount of sunlight that the plant receives. Sunlight is very important for plants, as it enables photosynthesis. Different plants require different amounts of sunlight, for optimal growth. 

**Intensity of green color:** this is a proxy for the growth of the plant. By capturing how much green there is in a picture of the plant, we can capture its vitality, and use this as an indicator of the general state of the plant. Of course, this is just a proxy measure, and will be accompanied by actual pictures of the plant. 
## Sensors Review
**Photosensitive Light Sensor Module**

**INSERT FIGURE 2 WITH TITLE AND SOURCE**

*Working principle*
This sensor works based on the concept of photoconductivity. The red tip with the wiggly wire is a photoresistor. We can see a sketch of its components in Figure 3.

**INSERT FIGURE 3 WITH TITLE AND SOURCE**

A photoresistor is made of a material that, when exposed to light, experiences a decrease in its resistivity. This translates to a change in the voltage output of the signal (Figure 4).

**INSERT FIGURE 4 WITH TITLE AND SOURCE**

*Specifications*

From Reference 5, we can gather the following specifications:
* working voltage: 3.3~5V
* output: digital switching (LOW or HIGH voltage on D pin) 
* analog signal (voltage output on A pin)
* output current >= 15mA, can directly light LED.

*Wiring schematic*

We are using the analog pin of the module, so we need to connect the module’s signal pin to one of the channels of the ADC. The wiring setup is expressed in Table 1

**INSERT TABLE 1 WITH TITLE AND SOURCE**

*Applicability*

It is worth noting that this light sensor is not calibrated, and that every sensor, even of the same brand and batch, is likely to output different values for the same period. Hence, this should only be used as an indicator of how much hours of sunlight the plant has received, rather than trying to quantify the actual value of light intensity. The sampling rate is practically irrelevant, since we will be measuring every minute, or every hour.

**DHT11 Temperature and Humidity Sensor Module**

**INSERT FIGURE 5 WITH TITLE AND SOURCE**

*Working principle*

To measure ambient humidity, the module has two electrodes embedded in a substrate that is capable of absorbing moisture. When there is more moisture in the environment, the substrate absorbs more vapor, which in turn allows it to shed more ions and hence lower its resistance.

To measure temperature, it uses a thermistor, which is a resistor that changes its resistance with temperature much more sensibly than a common resistor. 

We can see the inner components of the sensor in Figure 6.

**INSERT FIGURE 6 WITH TITLE AND SOURCE**

As we can see, the module has its own ADC, and it also saves the transfer function. Because of this, its output is already the temperature and humidity values. 

*Specifications*

The specifications of this output can be seen in Figure 7 (DHT11 column).

**INSERT FIGURE 7 WITH TITLE AND SOURCE**

*Wiring schematic*

The wiring setup is expressed in Table 2

**INSERT TABLE 2 WITH TITLE AND SOURCE**

*Applicability*

Since we expect the temperature and humidity to vary slowly, there is no need to sample at higher rates than 1Hz. Also, the humidity and temperature accuracy are enough for our home growing purposes.

**Soil Moisture Sensor Module**

**INSERT FIGURE 8 WITH TITLE AND SOURCE**

*Working principle*

This sensor works in exactly the same way as the humidity sensor. It consists of two electrodes embedded in a dielectric. The moisture in the soil changes the conductivity of the dielectric, and thus the output signal.

This sensor does not come with a built-in transfer function, and it outputs the voltage of the signal. We need to calibrate this sensor with a sample of the soil we intend to work with. To do this, we used Soil Moisture Sensor Calibration Method 1 in the Annex. For more representative results, one should use Method 2. However, due to not being able to collect a large enough soil sample, we opted for Method 1.

The resulting transfer function is a straight line between: 1234.1234V for 0% RH, and 1234.1324V for 100% RH.

*Specifications*

From Reference 4, we can gather the following specifications:
•	Operating Voltage: 3.3 ~ 5.5 V
•	DC Output Voltage: 0 ~ 3.0V
•	DC Operating Current: 5mA
•	Interface: PH2.0-3P
•	Dimensions: 3.86 x 0.905 inches (L x W)
•	Weight: 15g

*Wiring schematic*

The wiring setup is expressed in Table 3.

**INSERT TABLE 3 WITH TITLE AND SOURCE**

*Applicability*

Again, since the soil moisture is not expected to vary drastically, the sampling rate of this device is more than enough. Also, with proper calibration, the results should be good enough for the data to be usable for later analysis. The sensor if more than enough in terms of sampling speed capacity, since we are going to be taking samples every minute, or every hour.

**Camera Module**

**INSERT FIGURE 9 WITH TITLE AND SOURCE**

*Camera specifications*

**INSERT CAMERA SPECIFICATIONS IMAGE OR TABLE**

*Wiring schematic*

Connecting the camera is very simple, as can be seen in the next animation.

**INSERT FIGURE 10 WITH TITLE AND SOURCE**

#Signal conditioning and processing
Here, we will talk about how often we took samples for each sensor, and also how we decided to process and share the data. It is important to note that all the sensors we used have some kind of signal conditioning, and we will provide resources that show the structure of their circuit boards.
*	Signal conditioning within sensor modules

Temperature and Humidity sensor module circuit board: See Reference 10

Light sensor module circuit board: See Reference 9

Soil Moisture sensor module circuit board: See Reference 4

* Sensor Output Sample rates

The sample rate for the outputs that the sensors give (all except the camera) was one sample per hour. This is enough to capture the relevant fluctuations of the phenomena of interest. For the camera, we took a picture every 24 hs. This is also enough to monitor the state of the plant.

*	Data Storage and IoT integration

We decided to store the data locally, by writing it to a .csv file. This will make it easy for others to use the data if one decided to upload it somewhere. The pictures taken by the camera were also stored in a local folder. The code to do this is shown in Figure 11.

**Image with code.**

To share the data, we decided to tweet a daily summary of the data. To share this summary, we used the code in Figure 12. Instructions on how tweet using a Raspberry Pi can be found at Reference 6.

**Image with code.**

We also used the OpenChirp IoT platform to share our data in real time, and made use of its graphing capabilities. Instructions on how to use this platform with Raspberry Pi can be found at Reference 7. The code we used to do this is shown in Figure 13.

**Image with code.**

*	Data processing

Here, we explain how we processed the signals sampled by the sensors:

*Temperature and humidity sensor:* this sensor outputs temperature and humidity values, and so there is not much data processing necessary. The only problem we encountered was that it could give erroneous zero measures often. We decided to store the erroneous values as “NaN” entries, and let them be filtered by prospective data analysts. For the twitter summary, since we decided to use the average daily temperature and humidity, we used a special average function that did not include “Nan” values.

*Soil moisture sensor*: after calibration (Soil Moisture Sensor Calibration Method 1 in Annex), the transfer function was included in the main code. The sampled values were stored, and a daily average was tweeted.

*Light sensor*: after the calibration (Light Sensor Calibration in Annex), the transfer function was included in the main code. The sampled values were stored, and a daily average was tweeted.

*Camera*: to process the daily picture, we first configured the camera settings to take consistent pictures (instructions on how to do this can be found in Reference 8). We then extracted the RBG values from the picture, and cropped the matrix so as to fit the plant with as little background as possible. Then, the average value of the Green matrix was used as the “Green Vitality” indicator, and this was tweeted.

The code we used for data processing is shown in Figure 14.

**Image with code.**


## Progress Report: 10-5-20

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
- **Time permitting: time series graphics that may inform users how temperature/humidity/light/moisture affect basil plant performance 


## Github pages syntax (for reference)

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/lgraff/lgraff-12704_Final_Project/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

You can use the [editor on GitHub](https://github.com/lgraff/lgraff-12704_Final_Project/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.
