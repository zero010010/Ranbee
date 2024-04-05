# Eurostat API

This API works as a gateway to access and analyze employment data related to foreign nationals, sourced from the Eurostat database. It initiates the process by fetching the raw data from the Eurostat API. <br>
The API undertakes a series of data cleaning and preprocessing steps to refine and transform the retrieved information. Finally, the API exposes multiple endpoints that enable users to retrieve and visualize the processed employment statistics data for further analysis or exploration.<br>

## Endpoints

### 1. `/eurostat/`<br>

This endpoint retrieves data from the Eurostat API, performs data cleaning and preprocessing, and saves the processed data in different folders.<br>

**Response:**<br>

- Returns a message indicating that the setup is complete.<br>

- The processed data is saved in the following folders:
  - `data/raw`: Contains the raw data retrieved from the Eurostat API.<br>
  
  - `data/pre-processed`: Contains the data after initial cleaning and preprocessing.<br>
  
  - `data/processed`: Contains the final processed data, with additional transformations like calculating totals and handling missing values.<br>
  
  - `data/serie`: Contains the generated "EU" series data, which is likely an aggregated series for the European Union.<br>

### 2. `/eurostat/head`<br>

This endpoint provides a preview of the unprocessed data obtained from the Eurostat API by returning the initial five rows of the data frame.<br>

**Response:**<br>

- Returns a JSON representation of the first five rows of the raw data.<br>

### 3. `/eurostat/serie`<br>

This endpoint returns the first five rows of the processed "EU" series data.<br>

**Response:**<br>

- Returns a JSON representation of the first 5 rows of the processed "EU" series data.<br>

## Data Processing<br>

The API performs the following data processing steps:<br>

1. Retrieves data from the Eurostat API endpoint for the dataset, which contains quarterly employment statistics by nationality, age, and sex.<br>

2. Performs data cleaning and preprocessing, including:
   - Dropping unnecessary columns
   - Filling missing values with zeros
   - Rounding numerical values
   - Converting quarter values to specific month values
   - Filtering the data for foreign citizens and active employment status
   - Grouping the data by country and gender
3. Saves the processed data in different folders for further analysis or visualization.
4. Generates an aggregated "EU" series by summing the data across countries.

## Usage

1. Install requirements.txt
2. Run the FastAPI application.
3. Use the provided endpoints to access and visualize the processed Eurostat data.

Note: The API code includes additional helper functions and utilities for data processing and transformation, which are imported from the `util/funcionesEurostat.py` module.