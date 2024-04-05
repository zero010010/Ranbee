# Ranbee
A model based on ML techniques to predict a socio-economic variable in real-time using Big Data obtained from Eurosat, Google Trends and GDELT 

This README file provides an overview of the folder structure in this repository, along with a brief description of each folder's contents

# Project Folder Structure

├── Documentación<br>
│ ├── DIVISION EN MINI TAREAS.docx<br>
│ ├── DOCUMENTACION API GDELT.md<br>
│ ├── DOCUMENTACION API PYTRENDS.md<br>
│ ├── DOCUMENTACION CODE GDELT.md<br>
│ └── ESQUEMA PRIMERA REUNION RANDBEE.docx<br>
├── EUROSTAT<br>
│ ├── eurostatAPI.py<br>
│ ├── nuevos notebooks<br>
│ │ ├── eurostat.ipynb<br>
│ │ ├── eurostat2.ipynb<br>
│ │ └── eurostat3.ipynb<br>
│ ├── src<br>
│ │ ├── eurostat2.py<br>
│ │ └── funcionesEurostat.py<br>
│ └── util<br>
│ └── funcionesEurostat.ipynb<br>
├── GDELT<br>
│ ├── LLAMADAS A CADA ENDPOINT EJEMPLOS.docx<br>
│ ├── PRIMER MODELO API GDELT.ipynb<br>
│ ├── gdelt1.py<br>
│ ├── prueba funciones API gdelt.ipynb<br>
│ └── prueba gdelt.ipynb<br>
├── Gtrends<br>
│ ├── API PARA PYTRENDS.ipynb<br>
│ ├── Documentation<br>
│ │ ├── Gtrends(ES).md<br>
│ │ └── Gtrends.md<br>
│ └── Notebooks<br>
│ ├── pytrends_part0.ipynb<br>
│ └── pytrends_part1.ipynb<br>
├── Prueba Big Query<br>
│ └── prueba big query.sql<br>



## Folder Descriptions

- **Documentación**: Documentation files related to the project.


- **EUROSTAT**: Files and notebooks related to the Eurostat API.

The function of this API is to provide access to data from the Eurostat API, specifically related to employment statistics for foreigners by retreiving data from the Eurostat API endpoints and performing data cleaning and preprocessing steps, including dropping unnecessary column, filling missing values and so on.

Basically the API acts as an intermediary to fetch employment data for foreigners from the Eurostat API, clean and process the data, and provide endpoints to access and visualize the processed data.

- **GDELT**: Files and notebooks related to the GDELT API.

This API provides access to GDELT data and includes  endpoints to extract articles and obtain their tone and popularity. It also includes a data cleaning function for the retrieved data. Two versions of the API have been developed: one with the cleaning function integrated within the endpoint, and another with an independent call for final data cleaning.

- **Gtrends**: Files and notebooks related to the Google Trends API (pytrends).

This API provides access to Google Trends data using the unofficial Pytrends API. It includes endpoints to extract the average search volume for a defined topic within a specific time period.

Initially, the endpoints have been created with predefined dates and countries. However, the possibility of including countries and dates as parameters in the API calls or the extraction function is being considered, to provide more flexibility.

- **Prueba Big Query**: SQL test file for testing BigQuery.

This test query retrieves a sample of 1000 rows from the GDELT dataset related to the theme of "work". However, it's important to note that this was a test performed on Google Cloud, and the team hasn't decided yet whether to use this approach. 

Please refer to the individual files and folders for more specific information about their contents and purpose.




Clone this repo: `git clone https://github.com/zero010010/Ranbee.git`










