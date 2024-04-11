# FastAPI Application for Eurostat Data Extraction and Exploration

This FastAPI application provides endpoints for extracting data from the Eurostat API, preprocessing the data, and performing Exploratory Data Analysis (EDA) on the extracted data.

## Endpoints

### `/eurostat/`

This endpoint retrieves data from the Eurostat API, decompresses the data, and performs data cleaning and preprocessing steps.

#### Response

The endpoint performs the following tasks:

1. Sends a GET request to the Eurostat API endpoint to retrieve data related to the labor force survey.
2. Decompresses the received data and saves it as a CSV file.
3. Reads the decompressed CSV file into a Pandas DataFrame.
4. Creates a `data/raw` folder (if it doesn't exist) and saves the raw data as a CSV file.
5. Performs data cleaning and preprocessing steps:
   - Drops unnecessary columns from the DataFrame.
   - Fills NaN values with zero and rounds the `OBS_VALUE` column to one decimal place.
   - Creates a new `year_month` column based on the `TIME_PERIOD` column, mapping quarters to specific months.
   - Filters the data for foreigners with active status and dates after 2017.
6. Splits the data into separate DataFrames for each country and gender.
7. Removes countries with empty DataFrames or DataFrames with more than 50% zero values.
8. Saves the preprocessed data in the `data/preprocessed` folder.
9. Saves the processed data in the `data/processed` folder.
10. Completes the quarterly time series in the `data/processed` folder.
11. Generates a summary series for the European Union (EU) and saves it in the `data/serie` folder.
12. Returns a success message indicating that the setup is complete.

### `/eurostat/head`

This endpoint returns the first five rows of the raw Eurostat data in JSON format.

### `/eurostat/serie`

This endpoint returns the first five rows of the generated EU summary serie in JSON format.

### `/eda`<br>

This endpoint performs Exploratory Data Analysis (EDA) on the raw Eurostat data or the generated EU summary series, based on the provided `data_source` parameter.

#### Parameters<br>

- `data_source` (str): The source of the data for EDA.  The values are `"eurostat"` for the raw Eurostat data and `"serie"` for the generated EU summary serie.<br>

#### Response<br>

The endpoint performs the following tasks:<br>

1. Reads the specified data source (raw Eurostat data or EU summary serie) into a Pandas DataFrame.
2. Performs EDA on the DataFrame, including:<br>
   - Counting the number of rows and columns<br>
   - Listing the column names<br>
   - Counting the null values for each column<br>
   - Determining the data types of each column<br>
   - Calculating descriptive statistics<br>
3. Creates an `EDA` folder (if it doesn't exist).<br>
4. Saves the EDA results as a CSV file in the `EDA` <br>folder, with a unique filename based on the `data_source`.
5. Returns a message indicating the path of the saved EDA results file.

## Setup

1. Install requiured libraries 


2. Run the FastAPI application 


3. Access the application through the provided URLs: <br> eg:(`http://localhost:8000/eurostat/`,<br> 
`http://localhost:8000/eurostat/head`<br>,
 `http://localhost:8000/eurostat/serie`<br>,`http://localhost:8000/eda?data_source=eurostat`).

After running the API, you should find the processed data in the `data/raw`, `data/preprocessed`, `data/processed`, and `data/serie` folders, as well as the EDA results in the `EDA` folder.


