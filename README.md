
## 1 Project Objective

The objective of the project is to make wind predictions for a specific location with higher accuracy than that provided by general weather forecast models. 

Datasets of historical weather forecasts and historical weather measurements are going to be processed to train a selection of regression models using supervised machine learning techniques.

After an iterative process of training/testing techniques and feature engineering, the best model obtained is going to be captured to perform real-time wind predictions based on current weather forecast data captured from weather prediction APIs, hoping to improve its accuracy through that machine learning process.

A beta web application has been developed to display current weather forecasts in real time. 

## 2 Instructions for running the project:

* **1) Data download:** Download the data from the link : xxxx . Files should be copied within the folder of the local repository in a folder called Data/

* **2) The file environment.yml:** can be used to create an environment to run the files if needed.

* **3) Development phase :** The development phase of the project is done in the files: 1_DataPreparation.ipynb, 2_EDA.ipynb, 3 FeatEng.ipynb . They can be executed in the order 1,2,3. Each of the files will use some data in csv format from the folder Data/ and generate another csv at the end of the file, that will be used in the following file. Also, the file 3 FeatEng.ipynb will generate a model that will be saved within the route: /Data/model/windpredictor.sav that will be used in the deployment phase to make real-time predictions. 

* **4) Deployment phase :** The deployment phase (web application real time forecasts) is done in the files: app.py , app1.py, app2.py. To execute the app run from the terminal within the folder repository the following: > streamlit run app.py. 

## 3 Files in the repository

* **Wind Forecast Project Report.pdf** : Descriptive report of the project.

* **README.md** : Brief summary and instruction of how to execute the files in the repo.

* **1_DataPreparation.ipynb**
Jupyter-lab file. First file of the development phase, data preparation.

* **2_EDA.ipynb** : Jupyter-lab file. Second file of the development phase, E.D.A.

* **3 FeatEng.ipynb** : Jupyter-lab file. Third file of the development phase, Feature Engineering & Machine Learning.

* **environment.yml** : Environmental file with the dependencies needed to run the project

* **.gitigonre** : Hidden file to avoid uploading unwanted file to GitHub repository.

* **app.py** : 	Application with web interphase that process information from OpenWeather and AEMET APIs and create realtime weather forecasts for the study case location. To run the web app, execute from the terminal within the project folder: >streamlit run app.py

* **app1.py** :Sub-app inside app.py. Should not be executed directly.

* **app2.py** :Sub-app inside app.py. Should not be executed directly.

* **Data/model/windpredictor.sav** : Wind forecast machine learning model captured with pickle library.

* **Data/StationsRecords/DH-6001.csv** Weather station records located in Tarifa. 

* **Data/StationsRecords/DH-4554X.csv** Weather station closed to the target location. 

* **Data/StationsRecords/DH-6329.csv** Weather station closed to the target location.

* **Data/historicalForecast.csv** Historical weather forecasts. 


## Data Sources used

Two data sources have been merged:

Historical actual weather data: Historical weather measurements from AEMET weather stations. AEMET is the Spanish Government Weather Forecasting agency that has a wide range of metro Station deployed along the Spanish territory.

Link: https://opendata.aemet.es/centrodedescargas/inicio

Historical Weather Forecasts: Historical weather predictions from OpenWeatherData. OpenWeatherData according to their website generate s predictions based on GFS and ECMWF models applying already some machine learning optimization. Their predictions are going to be the baseline of the project, so the baseline is already going to be a challenge to overcome. Hopefully, as the project is very focused on one of the variables (wind) and on a specific location, there is still room for improvement.

Link: https://openweathermap.org/api
