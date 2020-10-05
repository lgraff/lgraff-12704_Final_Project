# 12-704 Final Project
# Hi-Tech Basil

## Introduction
## Motivation
## Goals

## Progress Report: 10-5-20

### Current Progress
- Set up the circuit for all sensors and confirmed that they are taking measurements when exposed to physical stimuli. This includes the temperature/humidity sensor, light sensor, and soil moisture sensor. The soil moisture sensor was something we purchased externally. We also tested that this circuit works specifically in the environment of the basil plant subject we're using.
- Wrote basic Python code to record the measurements of each sensor.
- Connected a camera to the circuit and wrote code to take repeated photos after a time interval
- Thought about which metrics would be appropriate to use as a measure of plant changes over time. One option is to just output a picture of the plant at each time step, letting the user define the relative growth. Two other more quantifiable options are: 1) plant height, which may be measured through height tick marks drawn behind the plant, and 2) the number/percentage/intensity of green pixels in the image.
- Investigated basic image processing in Python to understand the feasibility of the last two quantifiable options

### Problems Encountered
- Setting up the physical space - how to ensure that the sensors are directly next to the plant while also ensuring that the camera is far enough to capture the image of the full plant; it would also be helpful to have the photo of the plant be taken against a relatively blank backdrop

### Future Plan
- Determine how to convert the output voltage values of the soil moisture sensor to a soil moisture percentage. This link (https://www.switchdoc.com/2020/06/tutorial-capacitive-moisture-sensor-grove/) should be helpful.
- Learn more about basic image processing to see what data of interest we can extract from our images.
- Create a database to store the average temperature, humidity, light, and soil moisture values of the past 6 or 8 hours, along with a picture of the plant at that time step and possibly a measure of growth in the past 6 or 8 hours; This will require us to sense temp/humidity/light/moisture at relatively short intervals, take the average of the time interval, and then record the values. Each row of the database represents a time step.
- Determine how to connect everything to an IoT app and decide what to display to users. We imagine an app that can display a row of the database at each time step.
- *Time permitting: time series graphics that may inform users how temperature/humidity/light/moisture affect basil plant performance 


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
