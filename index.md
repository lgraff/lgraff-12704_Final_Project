# 12-740 Final Project
# Hi-Tech Basil

- [Video link](https://vimeo.com/471399257)
- [Twitter link](https://twitter.com/basil_tech)
- [OpenChirp link](https://openchirp.io/home/device/5f8b0735004d6e55c61dd4bb#visualization)

# Introduction
In this project, we describe how to set up a sensing and data broadcasting system for a homegrown basil plant. The data is captured by a Raspberry Pi and various sensors, and made available through Twitter, the IoT platform OpenChirp, and a .csv file. If enough people create this simple at-home system, we could crowdsource a useful database that offers insight into the optimal ranges for environmental factors that promote plant growth.
## Motivation
Growing plants indoors requires attention to a variety of environmental factors, including temperature, humidity, light, and soil moisture levels. Regulation of these parameters can be difficult, especially when there is sparse data concerning ideal growing conditions for individual plants. Specifically for the basil herb, a quick online search will reveal several different choices that an individual may make when tuning the ambient environmental factors. Notably, however, most sources are primarily anecdotal; homegrowers have yet to document the environmental conditions and associated growth patterns of their plants over time. To address these needs, we propose Hi-Tech Basil: a tweeting indoor basil plant with an associated database and IoT capabilities. Analyzing the hourly records of this database, in addition to visualizing photos of the plant included in live daily tweets [(@smart_basil)](https://twitter.com/basil_tech), may provide home growers with insight that optimizes the growth of their indoor plants.
## Project Sketch
Our setup is described in Figure 1.

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/New_Sketch.png">
</p>
<p align="center">
  Figure 1. Sensing and Data Broadcasting System sketch. Sources for figures: References 1,2,3
</p>

## Main Goal
* Create a sensing and data broadcasting system for homegrown plants so that users may extract information pertaining to the conditions necessary for plant growth  
## Specific Goals
*	Create a sensing system that measures ambient humidity and temperature, ambient light intensity, soil moisture, and takes a still photo of the plant at the end of each growth period.
*	Create a growth status index that can be automatically extracted from the picture taken.
*	Store the collected data in a .csv file and automatically tweet a summary of the daily surveyed data.
*	Integrate the setup to an IoT platform.
*	Show feasibility of the creation of a massive database by combining experiments by many individuals.
# Methodology
## Phenomena of Interest
The physical phenomena of interest include soil moisture, temperature, humidity, and light. Since all the phenomena of our experiments vary slowly in time, they can all be considered static in nature.

**Soil moisture:** Soil moisture percentage refers to the amount of water available in the soil. It can be measured as a ratio of volume of water per unit volume of soil, or as a ratio of water mass per unit mass of soil. We opt for the second measure because it is easier to measure, and so the calibration of the soil moisture sensor is easy to conduct at home. According to Reference 4, the water in soil is important for plant growth because it acts as a carrier of nutrients, helps in the photosynthesis and metabolic process of plants, and moderates soil temperature.

**Ambient humidity:** Ambient humidity is roughly defined as the amount of water in the air, relative to the maximum amount of water the air can hold at a given temperature. The strict definition is “the ratio of the actual water vapour pressure to the saturation water vapour pressure at the prevailing temperature" (Reference 5). The importance of this factor for plant growth relates to the photosynthesis and transpiration processes. In a dry environment, the plant tries to retain its water by closing its stomata, but in doing so, the plant simultaneously stifles its ability to intake CO2. In a highly humid environment, the plant cannot evaporate water at a fast enough rate. Consequently, an appropriate humidity level allows the plant to both photosynthesize and transpire so that it may grow (Reference 22).

**Ambient temperature:** The ambient temperature simply describes the temperature of area directly surrounding the plant. This factor affects many metabolic processes that plants undergo while growing. While photosynthesis, transpiration, and respiration typically accelerate at higher temperatures, the temperatures required for the germination and flowering processes depend on the individual plant. For this reason, we see the existence of seasonal crops, or those that can only survive during certain times of the year (Reference 7).

**Ambient light intensity:** Light intensity, measured in units of lux, is formally defined as the amount of "light that is emitted in unit time per unit solid angle" (Reference 23). Measuring light intensity near the plant tells us the amount of sunlight that the plant receives. Sunlight is vital for plants, as it enables photosynthesis. The amount of sunlight required for this process, however, varies by plant (Reference 24). While a basil grower would be more interested in knowing the hours of sunlight exposure for their plant, the average light intensity will suffice for this purpose of this project. 

**Intensity of green color:** The average green pixel intensity from the image of each plant is used as a crude proxy of plant growth. By capturing the quantity of green in an image, we can better understand the vitality and general state of the basil we are using as a test subject. The inherent assumption is that a healthier basil plant will be greener. While this metric is not perfect, we think it is a suitable proxy, particularly for basil. From our prior qualitative experiences with indoor basil harvesting, a more vibrant has bushier leaves (hence more green), while the leaves of a decaying basil plant will wilt (hence less green). We recognize that plant height could also be representative of plant growth, but we believe that green pixel intensity better captures the full plant in all dimenions. 

## Sensors Review
**Photosensitive Light Sensor Module**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%202.png">
</p>
<p align="center">
  Figure 2. Light Sensor Module. Source: Reference 8
</p>

*Working principle*
This sensor works based on the concept of photoconductivity. The red tip with the wiggly wire is a photoresistor. We can see a sketch of its components in Figure 3.

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%203.png">
</p>
<p align="center">
  Figure 3. Photoresistor basic composition. Source: Reference 9
</p>

A photoresistor is made of a material that, when exposed to light, experiences a decrease in its resistivity. This translates to a change in the voltage output of the signal (Figure 4).

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%204.png">
</p>
<p align="center">
  Figure 4. Example of Voltage Output vs. Photoresistor’s Resistance. Source: Reference 9
</p>

*Specifications*

From Reference 10, we can gather the following specifications:
* working voltage: 3.3~5V
* output: digital switching (LOW or HIGH voltage on D pin) 
* analog signal (voltage output on A pin)
* output current >= 15mA, can directly light LED.

*Wiring schematic*

We are using the analog pin of the module, so we need to connect the module’s signal pin to one of the channels of the ADC. The wiring setup is expressed in Table 1

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Table%201.png">
</p>
<p align="center">
  Table 1. Wiring Setup for Light Sensor Module. Source: Self
</p>

*Applicability*

We describe our calibration process of the light sensor in the Appendix. The light intensity output of the sensor will serve as a broad indicator of how many hours of sunlight the plant has received. The sampling rate is practically irrelevant, since we will be recording measurements every minute, and the signal is relatively static within this time frame.

**DHT11 Temperature and Humidity Sensor Module**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%205.jpg">
</p>
<p align="center">
  Figure 5. DHT11 Temperature and Humidity Sensor Module. Source: Reference 11
</p>

*Working principle*

To measure ambient humidity, the module has two electrodes embedded in a substrate that is capable of absorbing moisture. When there is more moisture in the environment, the substrate absorbs more vapor, which in turn allows it to shed more ions and hence lower its resistance.

To measure temperature, it uses a thermistor, which is a resistor that changes its resistance with temperature much more sensibly than a common resistor. 

We can see the inner components of the sensor in Figure 6.

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%206.jpg">
</p>
<p align="center">
  Figure 6. Inner structure of DHT11 Temperature and Humidity Module. Source: Reference 12
</p>

As we can see, the module has its own ADC, and it also saves the transfer function. Because of this, its output is already the form of temperature and humidity values. 

*Specifications*

The specifications of this output can be seen in Figure 7 (DHT11 column).

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%207.png">
</p>
<p align="center">
  Figure 7. Output specifications for DHT11. Source: Reference 12
</p>
  
*Wiring schematic*

The wiring setup is expressed in Table 2

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Table%202.png">
</p>
<p align="center">
  Table 2. Wiring Setup for DHT11 Temperature and Humidity Sensor Module. Source: Self
</p>

*Applicability*

Since we expect the temperature and humidity to vary slowly, there is no need to sample at higher rates than 1Hz. Also, the humidity and temperature accuracy are sufficient for our home growing purposes.

**Soil Moisture Sensor Module**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%208.png">
</p>
<p align="center">
  Figure 8. Soil Moisture Sensor. Source: Reference 13
</p>

*Working principle*

This sensor works in the same way as the humidity sensor. It consists of two electrodes embedded in a dielectric. The moisture in the soil changes the conductivity of the dielectric, and thus the output signal.

This sensor does not come with a built-in transfer function, and it outputs the voltage of the signal. We calibrated the sensor according to the Soil Moisture Sensor Calibration Method 1 in the Appendix. For more representative results, one should use Method 2. However, since we were not able to collect a large enough soil sample, we opted for Method 1.

The resulting transfer function is a straight line following the equation in the Appendix (see Soil Moisture Sensor Calibration Method 1).

*Specifications*

From Reference 14, we can gather the following specifications:

•	Operating Voltage: 3.3 ~ 5.5 V

•	DC Output Voltage: 0 ~ 3.0V

•	DC Operating Current: 5mA

•	Interface: PH2.0-3P

•	Dimensions: 3.86 x 0.905 inches (L x W)

•	Weight: 15g

*Wiring schematic*

The wiring setup is expressed in Table 3.

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Table%203.png">
</p>
<p align="center">
  Table 3. Wiring Setup for Soil Moisture Sensor Module. Source: Self
</p>

*Applicability*

Since the soil moisture is not expected to vary drastically, the sampling rate of this device is sufficient. Also, with proper calibration, the results should be accurate enough such that the data is usable for later analysis. The sensor has a sufficient sampling speed capacity, since we are going to be taking samples every minute, or every hour.

**Camera Module**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%209.png">
</p>
<p align="center">
  Figure 9. Camera Module. Source: Reference 15
</p>

*Camera specifications*

From Reference 20, we can gather the following specifications:

•	2592 x 1944 static pixel resolution

•	L 25mm x W 24mm x H 7.5mm

•	15 cm ribbon cable

•	Angle of view: 54 x 41 degrees

•	Field of view: 2.0 x 1.33 m at 2 m


*Wiring schematic*

Connecting the camera is very simple, as can be seen in the next animation.

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%2010.gif">
</p>
<p align="center">
  Figure 10. Camera module connection animation. Source: Reference 15
</p>

## Signal conditioning and processing
In this section, we describe our sampling rates, data processing steps, and data sharing capabilities. It is important to note that all the sensors we used have some kind of signal conditioning, and we will provide resources that show the structure of their circuit boards.

**Signal conditioning within sensor modules**

Temperature and Humidity sensor module circuit board: See Reference 16

Light sensor module circuit board: See Reference 17

Soil Moisture sensor module circuit board: See Reference 14

**Sensor Output Sample Rates**

The sample rate for all sensors (except the camera) was one sample per hour, or 0.0167 Hz. This is more than enough to capture the relevant fluctuations of the environmental phenomena of interest. For the camera, we took a picture every 24 hours. We chose a much lower sampling rate for the photos to avoid memory storage issues with the larger images. Still, these daily images were sufficient in allowing us to monitor the state of the basil plant due to the slow growth process.

**Data Storage and IoT integration**

We chose to store the data locally by writing it to a .csv file. This file includes a row for every timestamp containing any measurement, and a column for every type of raw measurement taken. As such, there are 6 columns: timestamp, temperature, humidity, soil moisture, light, and average green intensity. It must be noted that the green intensity column contains null values unless the timestamp represents the end of a full 24 hour period. The .csv format will facilitate usage of the data by others if we decided to upload file elsewhere. Furthermore, if others decided to embark on the same Hi Tech Plant project with their own indoor plant, this file format would enable simple data merges. This would subsequently provide resources for the plant growing community to start quantitatively analyzing best practices concerning environmental conditions. The pictures taken by the camera at the end of each period were also stored in a local folder. 

To share the data, we decided to tweet a daily summary of the data hosted by the Twitter handle [@smart_basil](https://twitter.com/basil_tech). This includes the average temperature, humidity, soil moisture, and light value of the past 24 hours, as well as the average green pixel intensity of the photo taken at the end of the period. Users may scroll through the Twitter feed for a visual understanding of how the basil plant looks every 24 hours, associated with a summary of the average environmental parameters the plant experienced. Instructions on how to tweet using a Raspberry Pi can be found at Reference 18.

We also used the OpenChirp IoT platform to share our data in real time, making use of its graphing capabilities. Users can check this platform to see time series graphs of the raw measurements in real time. This can be of use for plant growers who need quick updates on the status of the environmental conditions so that they can make required changes. For example, one might decide to water their plant while simultaneously monitoring the soil moisture levels on OpenChirp in order to ensure that they do not exceed the plant's water tolerance. Instructions on how to use this platform with Raspberry Pi can be found at Reference 19. 

**Data processing**

After sampling the signals, we conducted basic data processing to obtain the necessary information.

*Temperature and humidity sensor*: Since this sensor outputs the digital temperature and humidity values, there is not much data processing necessary. The only problem we encountered was the common appearance of erroneous zero measures. We decided to store the erroneous values as “NaN” entries in our .csv files so that they could be subsequently filtered by analysts of the data. For the daily average Twitter summary, we used the specific average function that excluded “NaN” values.

*Soil moisture sensor*: We calibrated the sensor (see Soil Moisture Sensor Calibration Method 1 in the Appendix) to find the transfer function. The sampled values, which were output in terms of voltage, were then appropriately converted to moisture percentages. A daily average of these percentages was used in the tweet.

*Light sensor*: We calibrated the sensor (see Light Sensor Calibration Procedure in the Appendix) to find the transfer function. The sampled values, which were output in terms of voltage, were then appropriately converted to lux values. A daily average of these lux values was used in the tweet.

*Camera*: To process the daily picture, we first configured the camera settings to take consistent pictures according to the method offered in Reference 15. This included fixing the camera exposure gains, white balance, brightness level, and contrast level. For recordkeeping, we also added a timestamp on the photo. To avoid background color noise, we cropped the image so as to only include the basil plant. We then extracted the RGB values for each pixel in the cropped image and took an average of the green values. In our daily tweet and .csv file, we termed this value "Average Green Intensity." 

## Final Setup

Our final code called "combined_sensors.py" can be found in the Github repository.

**Physical Setup:** the setup sketch in Figure 1 was materialized as can be seen in Figure 11.

**Photo of our setup**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/setup.JPG">
</p>
<p align="center">
  Figure 11. Physical setup
</p>

## Experiments and Results
After running our code to collect data for XX days, we got the following results:

**CSV Output file:** The .csv file contained all the data points, as expected, with the structure shown in Figure 12.

**Screencaps of .csv data**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Figure%205.jpg">
</p>
<p align="center">
  Figure 12. Sample output of .csv file
</p>

**Twitter:** Our program successfully tweeted an average summary of the environmental parameters of the past 24 hours. A representative tweet from the username [@smart_basil](https://twitter.com/basil_tech) can be seen in Figure 13.

**Screencaps of Twitter**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/Twitter_screenshot.png">
</p>
<p align="center">
  Figure 13. Sample tweet from @smart_basil
</p>

Each photo has the timestamp attached, and the caption includes average humidity, temperature, soil moisture, and light. Users can scroll through successive tweets for a visual representation of the basil's growth over time. By examining the associated caption, they can also get a hasty sense of the environmental conditions that the basil plant prefers. For a more quantitative view, they can analyze the data of the .csv file. A preliminary review of @smart_basil's Twitter page reveals that the plant performs better in better lighting condtions, though our initial results are certainly skewed by low-brightness photos. We can also make a tentative connection between temperature and soil moisture levels; as temperature increases, the soil dries out more, so it is imperative to stay vigilant of the soil moisture levels in warmer weather.
 
**Open Chirp:** Our program successfully connected live to the OpenChirp IoT platform. A sample of the resulting graphs can be seen in Figure 14.

**Screencaps of OpenChirp**

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/OpenChirp_screenshot.png">
</p>
<p align="center">
  Figure 14. Sample time series graphs from OpenChirp
</p>

The OpenChirp minute-by-minute time series visualizations of the raw measurements show users how the environmental parameters update in real time. These graphs are valuable because they allow users to monitor conditions and make adjustments to the plant's ambient conditions as necessary. For example, we can see that the beginning of the measurement period was marked by low light intensity levels. This aligns with our observations that the days were cloudy. In these cases, users may choose to turn on a UV plant light to simulate sunlgiht conditions. In addition, we see soil moisture levels drop at the end of the period, which we attribute to warmer weather that may have resulted in more water evaporation. Upon seeing this, the user may be prompted to water their plants in order to avoid wilting.


## Discussion

**Contributions**

Hi Tech Basil, which was motivated by the need to provide people with more precise data regarding the parameters that stimulate basil growth, served as a successful proof of concept for a sensing and data broadcasting system for a homegrown plant. We showed that users can monitor and display environmental conditions and basil performance via three different output forms: 1) flat .csv file, 2) daily summary tweet, and 3) real-time visualizations of measurements in the IoT platform OpenChirp. Each output form has a unique value. While the .csv file lends itself to more in-depth data analysis by allowing for different aggregations, OpenChirp is useful in the sense that users can instantly tune the ambient environmental parameters upon a quick perusal of measurement readings. The value in Twitter is its visual representation of the plant, in addition to the quick-read stream of daily summary tweets and photos. 

The ultimate idea is that, if enough users participate in the data collection process, we can start to crowd source information pertaining to the ideal growing conditions for a basil plant. Our simple setup provides the foundation for this objective to become a reality. The set of sensors used were inexpensive, functional, and easy to install. Also, user-friendly IoT platforms and Python libraries like Twython allow for easy data sharing and remote monitoring, which makes the idea of building large databases of these experiments feasible. 

**Limitations**

Aspects of the project that need improvement primarily concern the form and utility of the measurements. First, from a user perspective, users may prefer to know the number of hours and quality of sunlight exposure as opposed to the actual value of light intensity during the period. Given that users can only control plant placement and the switch of a UV plant light, this would be a more practical measurement. Second, the average green intensity measure is only of use as a relative measure of the state of the plant, and it is also highly contingent on consistency of images. We can only characterize this metric if we have many comparison data points (i.e. several Hi Tech Basil experiments) coming from the same camera setup. Regarding image consistency, one issue we had with our initial tweets was that photo was taken on cloudy days in low-light conditions. This resulted in dark photos with erroneously low average green intensity values. To address this problem, we set both the brightness and contrast level of the photo at 60%. The subsequent days saw much brighter images with higher green values, but these days were also sunny themselves, so it was difficult to isolate the effects of our new image parameters. Third, we did not characterize the soil we used in the most accurate way. This falls out of the scope of the project, but it is important to recognize because the soil organic content, soil texture and nutrient content are major factors that affect plant growth. Instructions on how to characterize the soil should be added by some specialist, and perhaps these measurements can be monitored as well.

**Future Work**

In future work, we may extend this idea to other homegrown plants and consider adding actuators like a water pump that keeps the soil moisture level at a certain value range, an air humidifier that controls the ambient moisture, and a UV plant light that turns on when the plant needs additional sunlight. We can also set up alerts for the home grower when levels get critical (e.g. when the green vitality index falls below a threshold, soil moisture is too low, temperature out of proper growing range). Finally, one could add an automatic size detection algorithm to the image processing part that allows the user to monitor plant height in real time.

## References

Reference 1

Clip art flower pot. (n.d.). Clipart Library. Retrieved October 22, 2020, from http://clipart-library.com/clipart/1660553.htm

Reference 2

Photography png. (n.d.). Clipart Library. Retrieved October 22, 2020, from http://clipart-library.com/clipart/k8ixbpbcp.htm

Reference 3

Tripod clipart. (n.d.). Clipart Library. Retrieved October 22, 2020, from http://clipart-library.com/clipart/433056.htm

Reference 4

Soil moisture importance. (2013, December 24). IEASSA. Retrieved October 22, 2020, from http://ieassa.org/en/soil-moisture-importance/

Reference 5

Relative humidity (RH). (n.d.). NFSA. Retrieved October 22, 2020, from https://www.nfsa.gov.au/preservation/preservation-glossary/relative-humidity-rh

Reference 6

Brookes, S. (2016, December 26). Why is Grow Room Humidity Important? Garden Culture Magazine. Retrieved October 22, 2020, from https://gardenculturemagazine.com/grow-room-humidity-important/#:~:text=If%20your%20grow%20room%20humidity,water%20out%20of%20the%20plant [Here](https://gardenculturemagazine.com/grow-room-humidity-important/#:~:text=If%20your%20grow%20room%20humidity,water%20out%20of%20the%20plant.)

Reference 7

How does the temperature affect the plant growth? (n.d.). Science Projects. Retrieved October 22, 2020, from https://www.scienceprojects.org/how-does-the-temperature-affect-the-plant-growth/#:~:text=Effect%20of%20temperature%20on%20plants&text=Temperature%20influences%20most%20plant%20processes,%2C%20transpiration%2C%20and%20respiration%20increase

Reference 8

1pcs Módulo Sensor Fotosensible de detección de Luz Fotorresistencia para Arduino. (n.d). Amazon. Retrieved October 22, 2020, from https://www.amazon.es/M%C3%B3dulo-Fotosensible-detecci%C3%B3n-Fotorresistencia-Arduino/dp/B00VUQ6CU0

Reference 9

Arduino lesson - Photoresistor. (n.d.). Kookye. Retrieved October 22, 2020, from https://kookye.com/2018/11/16/arduino-lesson-sound-detection-sensor-2/

Reference 10

Using light sensor module with Raspberry Pi. (n.d.). UUGear.Retrieved October 22, 2020, from http://www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi/

Reference 11

DHT11 Temperature and Humidity Sensor and the Raspberry Pi. (2017, September 21). Raspbberry Spy. Retrieved October 22, 2020, from https://www.raspberrypi-spy.co.uk/2017/09/dht11-temperature-and-humidity-sensor-raspberry-pi/

Reference 12

Arduino lesson - DHT11 Sensor. (n.d.). Kookye. Retrieved October 22, 2020, from https://kookye.com/2018/11/16/arduino-lesson-dht11-sensor/

Reference 13

Tutorial – Using Capacitive Soil Moisture Sensors on the Raspberry Pi. (2020, June 17). SwitchDoc Labs. Retrieved October 22, 2020, from https://www.switchdoc.com/2020/06/tutorial-capacitive-moisture-sensor-grove/

Reference 14

Capacitive Soil Moisture Sensor SKU:SEN0193. (2017, May 25). SigmaElectronica. Retrieved October 22, 2020, from https://www.sigmaelectronica.net/wp-content/uploads/2018/04/sen0193-humedad-de-suelos.pdf

Reference 15

Getting started with the Camera Module. (n.d.). Raspberry Pi. Retrieved October 22, 2020, from https://projects.raspberrypi.org/en/projects/getting-started-with-picamera

Reference 16

DHT11 Temperature Sensor. (n.d.). Components 101. Retrieved October 22, 2020, from https://components101.com/sites/default/files/component_datasheet/DHT11-Temperature-Sensor.pd

Reference 17

Light Sensing Module. (n.d.). Sunrom. Retrieved October 22, 2020, from https://www.sunrom.com/p/light-sensing-module-ldr

Reference 18

Getting started with the Twitter API. (n.d.). Raspberry Pi. Retrieved October 22, 2020, from https://projects.raspberrypi.org/en/projects/getting-started-with-the-twitter-api

Reference 19

Berges, M. & Chen, B. 4. Creating Your Owwn IoT Device. (2019). 12-740 Data Acquisition (Inferlab). Retrieved October 22, 2020, from https://inferlab.github.io/12740/tutorials/openchirp.html

Reference 20

Raspberry Pi Camera Video Module 5 Megap. (n.d.). Desert Cart. Retrieved October 22, 2020, from https://www.desertcart.us/products/160041787-raspberry-pi-camera-video-module-5-megapixel-1080-p-mini-webcam-sensor-ov-5647-for-raspberry-pi-model-a-b-b-r-pi-2-b-pi-3-b-3-b-and-pi-4-b

Reference 21

Finio, B. Science with a Smartphone: Measure light with lux. (2019, October 3). Scientific American. Retrieved October 22, 2020, from https://www.scientificamerican.com/article/science-with-a-smartphone-measure-light-with-lux/

Reference 22

How humidity affects the growth of plants. (n.d). Polygon Group. Retrieved October 22, 2020, from https://www.polygongroup.com/en-US/blog/how-humidity-affects-the-growth-of-plants/#:~:text=When%20conditions%20are%20too%20humid,and%20thrive%20in%20moist%20soil

Reference 23

The Editors of Encyclopedia Britanica. Luminous intensity. (n.d.). Britannica. Retrieved October 22, 2020, from https://www.britannica.com/science/luminous-intensity

Reference 24

Light Temperature and Humidity. (n.d.). Texas A&M AgriLife Extension. Retrieved October 22, 2020, from https://aggie-horticulture.tamu.edu/ornamental/a-reference-guide-to-plant-care-handling-and-merchandising/light-temperature-and-humidity/


## Appendix: Calibration Procedures
***Soil Moisture Calibration Method 1 (Source: Reference 14)***

1-	Make several measurements when the sensor is dry (in the air, not inserted in the soil). Average the values of voltage. This value will correspond to 0% RH.

2-	Dip the sensor in a glass of water, to the depth that you will insert it in the soil. Make several measurements, and average the values of voltage. This value will correspond 1to 100% RH.

3-	The transfer function will be an interpolation of the line that passes through these points

The resulting equation when we performed this method was the following:

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/eqnmoist.PNG">
</p>

***Soil Moisture Calibration Method 2 (Mass to Mass ratio)***

1-	Take a sample of 100 gr of the soil you are using. Make sure the sample is roughly representative of the whole mass in the pot.

2-	Dry the sample in the sun for a day or until completely dry. Place the sample in a recipient (e.g. a cup), and compact it to mimic the compaction level of the pot.

3-	Insert the sensor in the soil up to the depth you will use in the actual experiment, and take several measurements of voltage in dry soil. Average them, and store it as the value corresponding to 0% Mass/Mass.

4-	With plunger, add 5 ml of water to the soil, and mix it well. Recompact to mimic the compaction level of the pot. This should be done quickly, as moisture can escape to the air. Once mixed and recompacted in the recipient, reinsert the sensor and take several measurements of the voltage. Average them, and store this as the value corresponding to 5% Mass/Mass.

5-	Repeat step 4 to get the voltage values for 10, 15, 20,…% Mass/Mass, until saturation. Saturation occurs when the soil is no longer able to absorb water.

6-	Rescale the Mass/Mass percentages to RH percentages by dividing them by the Mass/Mass percentage that achieved saturation.

7-	The transfer function can be either a polynomial fit to the points, or a direct linear interpolation between the points.

***Light Sensor Calibration Procedure***

Calibrating the light sensor involved comparing voltage readings from the sensor with light intensity measurements taken from a Lux meter. To obtain a Lux meter, we downloaded a smartphone app called “LUX Light Meter FREE”, which detects light intensity via the phone’s camera. We then placed the light sensor and phone side-by-side in a cardboard box, folding the sides of the box so that light was only able to enter the box through ¼ of the top surface. The purpose of this setup was to ensure that we only captured the light directly hitting the surface of the sensor. This is in accordance with the recommendation of Reference 21, which suggests that the light sensor and light source should be perpendicular to each other. We recognize, however, that our process was not entirely accurate since the top surface was large enough to allow light to enter diagonally.

Once our setup was complete, we took 14 different measurements of voltage of Lux. The box was placed in different locations and another phone was used to directly shine bright lights on the sensors. These points were then plotted in Figure 15 below below: 

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/CalibA.png">
</p>
<p align="center">
  Figure 15. Light calibration, linear scale
</p>

We observe a nonlinear relationship between voltage and Lux. We then transform the axes to a log-log scale, as shown in Figure 16.

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/CalibB.png">
</p>
<p align="center">
  Figure 16. Light calibration, log-log scale
</p>

The transformed scale exposes a relatively linear relationship between log(voltage) and log(lux). We perform a least squares linear fit and find the following relationship: 

<p align="center">
  <img src="https://github.com/lgraff/lgraff-12740_Final_Project/blob/gh-pages/eqnlight.PNG">
</p>

Using this relationship, we can convert between the sensor’s voltage value and a light intensity value that will be displayed to users.




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
