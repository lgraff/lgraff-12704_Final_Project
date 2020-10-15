# 12-740 Final Project
# Hi-Tech Basil

## Introduction
In this project, we describe how to set up a sensing and data broadcasting system for any homegrown plant. The data is captured by the Raspberry Pi and sensors, and made available through twitter, an IoT platform, and a .csv file, for people to use. If enough people do the same, we would then be able to have a very useful database to find the optimal ranges for all the factors that promote growth of plants.
## Motivation
Growing plants indoors requires attention to a variety of environmental factors, including temperature, humidity, light, and soil moisture levels. Regulation of these parameters can be difficult, especially when there is sparse data concerning ideal growing conditions for individual plants. Specifically for the basil herb, a quick online search will reveal several different choices that an individual may make when tuning the ambient environmental factors. Notably, however, most sources are primarily anecdotal; homegrowers have yet to document the environmental conditions and associated growth patterns of their plants over time. To address these needs, we propose Hi-Tech Basil: a tweeting indoor basil plant with an associated database, and IoT capabilities. Analyzing the hourly records of this database, in addition to visualizing photos of the plant included in live daily tweets, may provide home growers with insight that optimizes the growth of their indoor plants.
## Project Sketch
Our setup is described in Figure 1.
INSERT FIGURE 1 WITH TITLE AND SOURCE
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
*	Soil moisture: this is basically the amount of water available in the soil. It can be measured as a ratio of volume of water per unit volume of soil, or as a ratio of water mass per unit mass of soil. We opt for the second measure because it is easier to measure, and so the calibration of the soil moisture sensor is easy to do at home. The importance of this variable for plant growth is widely known. Here, I quote a passage from Reference 1:

“…

Importance of Soil Water:

-Soil water serves as a solvent and carrier of food nutrients for plant growth

-Yield of crop is more often determined by the amount of water available rather than the deficiency of other food nutrients

-Soil water acts as a nutrient itself

-Soil water regulates soil temperature

-Soil forming processes and weathering depend on water

-Microorganisms require water for their metabolic activities

-Soil water helps in chemical and biological activities of soil

-It is a principal constituent of the growing plant

-Water is essential for photosynthesis

…”
*	Ambient humidity: roughly defined as the amount of water in the air, relative to the maximum amount of water the air can hold at a given temperature. The strict definition is taken from Reference 2:
“…
The relative humidity (RH) is the ratio of the actual water vapour pressure to the saturation water vapour pressure at the prevailing temperature. For example – if a cubic metre can hold 100ml of water at 20 degrees centigrade (273 K) and it does contain 100ml then it is said to be 100% RH. If the same cubic metre of air at the same temperature only contains 50mls of water then it is described as 50% RH.
…”
The importance of this factor from plant growth is explained in the next passage, taken from Reference 3:
“…
If your grow room humidity is low (dry), it causes the plants to transpire much more rapidly than in a higher humidity environment. When this happens, the leaves become flaccid and begin to wilt, and over a longer period of time the plant will close its stomata, and reduce the flow of water out of the plant. This is very effective at stopping water loss, but unfortunately, it also reduces the intake of CO2. Without an adequate supply of CO2, the cells will begin to die, and the plant will look tired and ill.
…”
*	Ambient temperature: this is just the temperature of the room in which the plant is. This factor affects most plant processes. The next passage is taken from Reference 4:
“…
Temperature influences most plant processes, including photosynthesis, transpiration, respiration, germination, and flowering. As temperature increases (up to a point), photosynthesis, transpiration, and respiration increase.
…”
*	Ambient light intensity: measuring light intensity near the plant will give us the amount of sunlight that the plant receives. Sunlight is very important for plants, as it enables photosynthesis. Different plants require different amounts of sunlight, for optimal growth. 
*	Intensity of green color: this is a proxy for the growth of the plant. By capturing how much green there is in a picture of the plant, we can capture its vitality, and use this as an indicator of the general state of the plant. Of course, this is just a proxy measure, and will be accompanied by actual pictures of the plant. 



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
