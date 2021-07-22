# IMPORTS

import requests
import pandas as pd
import numpy as np
import datetime as dt
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from PIL import Image


#### 1. CALCULATIONS

# Function to transform wind in knots

def wind_knots(speed):
    return speed * 1.94384

# Function that return the linear component of an angular direction

def wind_components(wind_direction):
    NS_component = np.cos(np.radians(wind_direction))
    EW_component = np.sin(np.radians(wind_direction))
    return NS_component, EW_component

# Variables

lat = 36.013985
lon = -5.59883
API_key = '3c08d56033dbf63eb861caf5c5e30ccd'
units = 'metric'

# API Call

url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units={}".format(lat,lon ,API_key ,units)
r = requests.get(url)
json = r.json()

#   PREPARATION OF THE DATAFRAME

# Hourly Forecast Dataframe

hourly_forecast = pd.DataFrame.from_dict(json['hourly'])

# Correcting columns different names

hourly_forecast.rename(columns={'temp':'temperature'}, inplace=True)


#Selecting just the right columns (rain appear in json files just when is forecasted)

hourly_forecast = hourly_forecast[['dt', 'temperature', 'pressure', 
                                    'humidity', 'dew_point', 'clouds',
                                   'wind_speed', 'wind_deg', 'wind_gust']]

# Adding rain when appears in the API call

for i in range(0,len(json['hourly'])):
    if 'rain' in json['hourly'][i].keys():
        hourly_forecast.loc[i,'rain'] = json['hourly'][i]['rain']
    else:
        hourly_forecast.loc[i,'rain'] = 0

# Datetime format

hourly_forecast['dt'] = pd.to_datetime(hourly_forecast['dt'], unit = 's')

# Adding Cest Time

hourly_forecast['cest_time'] = hourly_forecast['dt'] + dt.timedelta(hours=2)

# Wind speed in knots

hourly_forecast['wind_speed'] = wind_knots(hourly_forecast['wind_speed'])
hourly_forecast['wind_gust'] = wind_knots(hourly_forecast['wind_gust'])

# Wind direction components

(hourly_forecast['Direction N-S'], hourly_forecast['Direction E-W']) = wind_components(hourly_forecast['wind_deg'])


# (daily) Seasonal Features creation

for i in hourly_forecast.index:
    hourly_forecast.loc[i,'hour'] = hourly_forecast.loc[i,'dt'].hour

period = 24

for i in hourly_forecast.index:
    hourly_forecast.loc[i,'s-24'] = np.sin(2*np.pi*hourly_forecast.loc[i,'hour']/period)
    hourly_forecast.loc[i,'c-24'] = np.cos(2*np.pi*hourly_forecast.loc[i,'hour']/period)

# Load the forecasting model
filename = 'Data/model/windpredictor.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# We maintain the same variables in the same order as when we train the model

features = hourly_forecast.loc[:,['temperature', 'dew_point', 'pressure','humidity', 'clouds',
                     'wind_speed', 'rain','Direction N-S', 'Direction E-W',
                     's-24', 'c-24']]

hourly_forecast['wind_forecasted'] = loaded_model.predict(features)

# Finding sunrise & sunsets

sunsets = date2num(list(filter(lambda x: x.hour==22, hourly_forecast['cest_time'])))
sunrises = date2num(list(filter(lambda x: x.hour==7, hourly_forecast['cest_time'])))

first_date = date2num(hourly_forecast['cest_time'].min())
last_date = date2num(hourly_forecast['cest_time'].max())

if len(sunsets)% 2 != 0: # If chart start during night period
    sunsets = np.append(first_date, sunsets)
    sunrises = np.append(sunrises, last_date)

#### 2- APLICATION
    
def app():
    image = Image.open('Data/images/forecast.jpeg')

    st.markdown("<h1 style='text-align: center; color: DodgerBlue;'>TARIFA ACCURATE WIND PREDICTOR</h1>", unsafe_allow_html=True)
    st.image(image, use_column_width = True)

    
    # Wind Plot

    fig, ax = plt.subplots(figsize=(12,6))

    ax.grid(True, which='both')
    ax.set_title('Tarifa Wind Accurate Forecast (Next 48h)')
    ax.set_ylabel('Wind Speed (knots)')


    z1= sns.lineplot(x='cest_time',y='wind_forecasted',data=hourly_forecast, ax=ax, label ='Accurate Wind Predictor');
    z2= sns.lineplot(x='cest_time',y='wind_speed',data=hourly_forecast, ax=ax, label ='Open Weather Forecast');
    

    # Timeline format

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%d/%m'))

    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[0,3,6,9,12,15,18,21]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))

    plt.xticks(weight = 'bold')

    # Darkening nights

    for i in range(0,len(sunsets)):
        ax.axvspan(sunsets[i],
                   sunrises[i],
                   color="grey", alpha=0.3)

    # Arrows with color code

    for i in range(0,47,3):

        if hourly_forecast.loc[i,'wind_forecasted']>11:
            force = 'green'
        elif hourly_forecast.loc[i,'wind_forecasted']>=6 and hourly_forecast.loc[i,'wind_forecasted']<11:
            force = 'gold'
        else:
            force ='red'

        ax.quiver(hourly_forecast.loc[i,'cest_time'],0,
                    -hourly_forecast.loc[i,'Direction E-W'], -hourly_forecast.loc[i,'Direction N-S'], 
                    color=force, scale=(20/hourly_forecast.loc[i,'wind_forecasted']+20))

    st.pyplot(fig)

    # Weather Plot

    fig, ax = plt.subplots(figsize=(12,4))
    ax2=ax.twinx()

    ax.grid(True, which='both')
    ax.set_title('Tarifa Weather (Next 48h)')
    ax.set_ylabel('Clouds (%)')
    ax2.set_ylabel('Temperature (ºC)')

    ax.set_ylim(0,100)
    ax2.set_ylim(0,30)

    # Darkening nights

    for i in range(0,len(sunsets)):
        ax.axvspan(sunsets[i],
                   sunrises[i],
                   color="grey", alpha=0.3)


    z1 = sns.lineplot(x='cest_time',y='temperature',data=hourly_forecast, ax=ax2, color = 'r', label='Temperature');

    z2 = ax.bar(x='cest_time',height='clouds',data=hourly_forecast, color = 'grey', width=0.2);

    st.pyplot(fig)

    # Rain Plot

    fig, ax = plt.subplots(figsize=(12,2))

    ax.grid(True, which='both')
    ax.set_title('Tarifa Weather (Next 48h)')
    ax.set_ylabel('Rain (mm/h)')
    ax.set_ylim(0,5)

    # Darkening nights

    for i in range(0,len(sunsets)):
        ax.axvspan(sunsets[i],
                   sunrises[i],
                   color="grey", alpha=0.3)

    z2 = ax.bar(x='cest_time',height='rain',data=hourly_forecast, color = 'grey', width=0.2);

    st.pyplot(fig)