import streamlit as st

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

#### CALCULATIONS - METEO STATION REAL WIND
    
    # Function to transform wind in knots

def wind_knots(speed):
    return speed * 1.94384
    
    # API CAll to AEMET Anemometer

url_aemet = "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/6001"

querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqYXZpZXJsaXJvQGdtYWlsLmNvbSIsImp0aSI6ImJlNDk5MGJmLWI3NGItNDVhZi1hMzFiLWVhNTczOWVhZDQ5NCIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjIwODA1NDQxLCJ1c2VySWQiOiJiZTQ5OTBiZi1iNzRiLTQ1YWYtYTMxYi1lYTU3MzllYWQ0OTQiLCJyb2xlIjoiIn0.haVMyUZcNfyDl69AfjDd6W5vB7xBOUZrFDpWRgXAfHM"}

headers = {
    'cache-control': "no-cache"
    }

r_aemet = requests.request("GET", url_aemet, headers=headers, params=querystring)

url2 = r_aemet.json()['datos']

r_aemet = requests.get(url2)

json_aemet = r_aemet.json()


# CREATING OBSERVATION DATAFRAME

actual_weather = pd.DataFrame.from_dict(json_aemet)

# Select just important columns

actual_weather = actual_weather[['fint', 'vv','dv']]

# Rename Columns

actual_weather.rename(columns={'vv':'wind_speed', 'dv': 'wind_direction'}, inplace=True)

# Datetime format

actual_weather['fint'] = pd.to_datetime(actual_weather['fint'])

# Adding Cest time

actual_weather['cest_time'] = actual_weather['fint'] + dt.timedelta(hours=2)

# Wind in Knots 

actual_weather['wind_speed'] = wind_knots(actual_weather['wind_speed'])

### WEB APLICATION


def app():
    
    image = Image.open('Data/images/anemometer.jpeg')
    st.markdown("<h1 style='text-align: center; color: DodgerBlue;'>TARIFA WEATHER STATION - ANEMOMETER</h1>", unsafe_allow_html=True)
    st.image(image, use_column_width = True)
    
    
    # Realtimewind Plot

    # Figure setup

    fig, ax = plt.subplots(figsize=(12,8))
    ax.grid(True, which='both')
    ax.set_title('Tarifa Meteo Station - Wind Meassured last 24h')
    ax.set_ylabel('Wind Speed (knots)')

    # Timeline format

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%d/%m'))

    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[0,3,6,9,12,15,18,21]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))

    plt.xticks(weight = 'bold')

    # Plot

    z1= sns.lineplot(x='cest_time',y='wind_speed',data=actual_weather, ax=ax);

    st.pyplot(fig)