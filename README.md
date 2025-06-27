# ETL and visualization for ANP fuel dataset
Welcome to my first Dash project!

This is how I envision a fuel price dataset held by the ANP (National Petrol and Gas Agency) could be used.
The original dataset contains the daily price for gas stations in Brazil, all regions, starting from year 2004.

I started this in the mid of 2025-May, when I got my hands on two Udemy courses, plotly-dash and pandas
A few updates will follow on this page (newest to oldest), so one can have a glimpse on the progress.

2025-Jun-27

I fused what I learned with my own ideas (and struggles) and cooked this visualization. It all started much like how I saw in the course, with a JupyterNotebook implementation.
But that surely was not enough for what I want to be a real online project (in the near future), so I changed my approach to decentralized Python scripts and more classes and methods.
Here's how it looks like so far:

![image](https://github.com/user-attachments/assets/8c90d9a8-257f-443f-aa75-71be1a2bccd3)

I bring two plots with basic information.
- Line chart - how the average fuel price behave over time, for all cities;
- Table - a breakdown for the price behavior for each city, fuel type in each year.

My design choice was to pop from the "sandwich menu" button a sidebar on the left, containing all the filters available, like so:

![image](https://github.com/user-attachments/assets/17542725-cfca-45e2-8070-75d4359ca51c)

Next I'll introduce KPIs. Then I'll have the project running online on some free platform.
