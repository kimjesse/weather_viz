#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false; // disable scroll bar when displaying Folium map\n}')


# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Global Historical Climatology Network daily (GHCNd)](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe - it's a wonderfully large dataset to play with! In particular, you will be asked to use data from the Ann Arbor Michigan location (my home!). and this is stored in the file: `assets/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`
# 
# Each row in this datafile corresponds to a single observation from a weather station, and has the following variables:
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write a python notebook which plots line graphs of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015. (Based on the graph, do you think extreme weather is getting more frequent in 2015?)
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# I've written some steps I think would be good to go through, but there are other ways to solve this assignment so feel free to explore the pandas library! What I really want to see is an image that looks like this sketch I drew at my desk:
# 
# ![](assets/chris_sketch.png)

# In[2]:


#  I'll be using the folium package to render the data into a map in Jupyter.

import folium
import pandas as pd

# get the location information for this dataset
df = pd.read_csv('assets/BinSize_d400.csv')
station_locations_by_hash = df[df['hash'] == 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89']

# get longitude and lattitude to plot
lons = station_locations_by_hash['LONGITUDE'].tolist()
lats = station_locations_by_hash['LATITUDE'].tolist()

# plot on a beautiful folium map
my_map = folium.Map(location = [lats[0], lons[0]], height = 500,  zoom_start = 9)
for lat, lon in zip(lats, lons):
    folium.Marker([lat, lon]).add_to(my_map)

# render map in Jupyter
display(my_map)


# ## Step 1
# Load the dataset and transform the data into Celsius (refer to documentation) then extract all of the rows which have minimum or maximum temperatures.
# 
# __hint: when I did this step I had two DataFrame objects, each with ~80,000 entries in it__

# In[3]:


import pandas as pd
df = pd.read_csv('assets/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df.head()


# In[4]:


# In this code cell, transform the Data_Value column
df['Data_Value'] = df['Data_Value'] / 10
maxes = df[df['Element'] == 'TMAX']
mins = df[df['Element'] == 'TMIN']


# ## Step 2
# In order to visualize the data we would plot the min and max data for each day of the year between the years 2005 and 2014 across all weather stations. But we also need to find out when the min or max temperature in 2015 falls below the min or rises above the max for the previous decade.
# 
# If you did step 1 you have two Series objects with min and max times for the years 2005 through 2015. You can use Pandas `groupby` to create max and min temperature Series objects across all weather stations for each day of these years, and you can deal with the records for February 29 (the leap year) by dropping them.
# 
# __hint: when I finished this step, I had two DataFrame objects, each with exactly 4015 observations in them__

# In[5]:


# create a DataFrame of maximum temperature by date
max_all = maxes.groupby('Date').max().reset_index()
max_all = maxes[~maxes['Date'].isin(['2008-02-29','2012-02-29'])]
# create a DataFrame of minimum temperatures by date
min_all = mins.groupby('Date').min().reset_index()
min_all = mins[~mins['Date'].isin(['2008-02-29','2012-02-29'])]


# ## Step 3
# Now that you have grouped the daily max and min temperatures for each day of the years 2005 through 2015, you can separate out the data for 2015. Then you can use the Pandas `groupby` function to find the max and min of the temperature data for each __day of the year__ for the 2005-2014 data.
# 
# __hint: at the end of this step I had two DataFrames, one of maximum and the other of minimum values, which each had 365 observations in them. I also had another pair of similar DataFrames but only for the year 2015.__

# In[6]:


# calculate the minimum and maximum values for the day of the year for 2005 through 2014
max_all['day'] = max_all['Date'].str.split('-',n=1).map(lambda x: x[1])
max_all['year'] = max_all['Date'].str.split('-',n=1).map(lambda x: x[0])
max_prev = max_all[max_all['year'] != '2015']
max_days_prev = max_prev.groupby('day').max()
min_all['day'] = min_all['Date'].str.split('-',n=1).map(lambda x: x[1])
min_all['year'] = min_all['Date'].str.split('-',n=1).map(lambda x: x[0])
min_prev = min_all[min_all['year'] != '2015']
min_days_prev = min_prev.groupby('day').min()
# calculate the minimum and maximum values for the years 2015
max_2015 = max_all[max_all['year'] == '2015']
min_2015 = min_all[min_all['year'] == '2015']
max_days_2015 = max_2015.groupby('day').max()
min_days_2015 = min_2015.groupby('day').min()


# ## Step 4
# Now it's time to plot! You need to explore matplotlib in order to plot line graphs of the min and max temperatures for the years 2005 through 2014 and to scatter plot __only__ the daily 2015 temperatures that exceeded those values.

# In[7]:


#Get Outliers
colder = pd.merge(min_days_prev,min_days_2015,on=('day'))
colder = colder[colder['Data_Value_x'] > colder['Data_Value_y']]
hotter = pd.merge(max_days_prev,max_days_2015,on=('day'))
hotter = hotter[hotter['Data_Value_x'] < hotter['Data_Value_y']]


# In[83]:


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from calendar import month_abbr
# put your plotting code here!
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
plt.xlabel('Time of Year')
plt.ylabel('Temperature in $\degree$C')
plt.title('Highest and Lowest Recorded Temperatures for Days of the Year (2005-2015)')
plt.plot(pd.to_datetime(max_days_prev.index,format='%m-%d').strftime('%m-%d'),max_days_prev['Data_Value'],color='xkcd:light red',alpha = 0.5)
plt.plot(pd.to_datetime(min_days_prev.index,format='%m-%d').strftime('%m-%d'),min_days_prev['Data_Value'],color='xkcd:light blue',alpha = 0.75)
plt.scatter(pd.to_datetime(hotter.index,format='%m-%d').strftime('%m-%d'),hotter['Data_Value_y'],marker='^',color='xkcd:blood red')
plt.scatter(pd.to_datetime(colder.index,format='%m-%d').strftime('%m-%d'),colder['Data_Value_y'],marker='v',color='xkcd:dark blue')
plt.gca().fill_between(range(len(max_days_prev)), 
                       max_days_prev['Data_Value'], min_days_prev['Data_Value'], 
                       facecolor='xkcd:silver',
                       hatch='/',
                       alpha=0.25)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_xticks(ax.get_xticks()[:-1])
plt.xlim(left=-1,right=366)
plt.legend(['Highest Recorded before 2015', 'Lowest Recorded before 2015','Days in 2015 Hotter than Previous Years','Days in 2015 Colder than Previous Years'],loc=0)
plt.gca().spines.values()
ax.spines[['right', 'top']].set_visible(False)
plt.savefig('jesse_assignment2.jpeg',facecolor='white', transparent=False,)

