# Ranbee
A model based on ML techniques to predict a socio-economic variable in real-time using Big Data obtained from Eurosat, Google Trends and GDELT 

This README file provides an overview of the folder structure in this repository, along with a brief description of each folder's contents

# Project Folder Structure


## Folder Descriptions<br>

# Ranbee

A model based on ML techniques to predict a socio-economic variable in real-time using Big Data obtained from Eurostat, Google Trends, and GDELT.

This README file provides an overview of the folder structure in this repository, along with a brief description of each folder's contents.

## Folder Descriptions

- **DOCUMENTATION**: Documentation files related to the project.

- **EUROSTAT**: Files and notebooks related to the Eurostat API.

The function of this API is to provide access to data from the Eurostat API, specifically related to employment statistics for foreigners by retrieving data from the Eurostat API endpoints and performing data cleaning and preprocessing steps, including dropping unnecessary columns, filling missing values, and so on.

Basically, the API acts as an intermediary to fetch employment data for foreigners from the Eurostat API, clean and process the data, and provide endpoints to access and visualize the processed data.

- **GDELT**: Files and notebooks related to the GDELT API.

This API provides access to GDELT data and includes endpoints to extract articles and obtain their tone and popularity. It also includes a data cleaning function for the retrieved data. Two versions of the API have been developed: one with the cleaning function integrated within the endpoint, and another with an independent call for final data cleaning.

- **GTRENDS**: Files and notebooks related to the Google Trends API (pytrends).

This API provides access to Google Trends data using the unofficial Pytrends API. It includes endpoints to extract the average search volume for a defined topic within a specific time period.

Initially, the endpoints have been created with predefined dates and countries. However, the possibility of including countries and dates as parameters in the API calls or the extraction function is being considered, to provide more flexibility.

- **BIG QUERY TEST**: SQL test file for testing BigQuery.

This test query retrieves a sample of 1000 rows from the GDELT dataset related to the theme of "work". However, it's important to note that this was a test performed on Google Cloud, and the team hasn't decided yet whether to use this approach.

- **DATA CLEANING**: Contains a ZIP file with data cleaning scripts for GDELT and Google Trends data.

- **MEMOIR**: Contains documents related to the project memoir, including drafts and task division files.

- **MODELS**: Contains notebooks and scripts related to the machine learning models used in the project.

Please refer to the individual files and folders for more specific information about their contents and purpose.

## Project Folder Structure
├── BIG QUERY TEST<br>
│
├── DATA CLEANING<br>
│ └── DATOS GDELT Y GTREND.zip<br>
├── DOCUMENTATION<br>
│ ├── EUROSTAT_API.md<br>
│ ├── GDELT_API.md<br>
│ └── GTRENDS_API.md<br>
├── EUROSTAT<br>
│ ├── Eurostat_API(c).py<br>
│ ├── eurostatAPI.py<br>
│ ├── eurostatAPI_EDA_TEST.py<br>
│ ├──<br>
│ ├── src<br>
│ │ ├── eurostat2.py<br>
│ │ └── funcionesEurostat.py<br>
│ └── util<br>
│ ├── funcionesEurostat.ipynb<br>
│ ├── funcionesEurostat.py<br>
│ └── funcionesEurostat2.py<br>
├── GDELT<br><br>
│ ├── Antiguas Versiones API<br>
│ │ ├── GDELT_API(C).py<br>
│ │ ├── PRIMER MODELO API GDELT.ipynb<br>
│ │
│ ├── GDELT_API.py<br>
│ ├── GDELT_API_org.py<br>
│ ├── LLAMADAS A CADA ENDPOINT EJEMPLOS.docx<br>
│ ├── Notebooks<br>
│ │
│ └── data<br>
│ └── final<br>
│ ├── gdelt_monthly.csv<br>
│ └── gdelt_quaterly.csv<br>
├── GTRENDS<br>
│ ├── API PARA PYTRENDS.ipynb<br>
│ ├── Documentationv
│ │ ├── Gtrends(ES).md<br>
│ │ └── Gtrends.md<br>
│ ├── Notebooks<br>
│ │
│ └── data<br>
│ └── final<br>
│ ├── gtrend_monthly.csv<br>
│ ├── gtrend_monthly_2017.csv<br>
│ ├── gtrend_quaterly.csv<br>
│ └── gtrend_quaterly_2017.csv<br>
├── MEMOIR<br>
│ ├── Ranbee_Memoir_DRAFT (1).docx<br>
│ ├── Ranbee_Memoir_DRAFT (1).pdf<br>
│ └── TEAM_TASKS<br>
│ ├── DIVISION EN MINI TAREAS.docx<br>
│ ├── ESQUEMA PRIMERA REUNION RANDBEE.docx<br>
│ └── Trello_board.pdf<br>
├── MODELS<br>
│ ├── modelAPI.ip<br>


## Contacts<br>

- cjimpar@gmail.com<br>
- juanmiguelopezpinero@icloud.com<br>
- ricardogotal@gmail.com<br>


Clone this repo: `git clone https://github.com/zero010010/Ranbee.git`<br>










