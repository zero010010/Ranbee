# GDELT API

This API provides access to data from the Global Database of Events, Language, and Tone (GDELT). It includes endpoints for retrieving articles, tones, and popularity information based on specified filters.

## Endpoints

### 1. `/articles/`

Retrieves articles from the GDELT database based on the provided filters.

**Parameters:**<br>

- `keyword` (str): The keyword to search for in the articles.<br>

- `start_date` (str): The start date for the article search (YYYY-MM-DD format).<br>
- `end_date` (str): The end date for the article search (YYYY-MM-DD format).<br>
- `country` (str): The country or list of countries to filter the articles by.<br>

**Response:**
- Returns a pandas DataFrame containing the retrieved articles.
- The DataFrame is saved as a CSV file<br> (e.g., `csv_articulos_1.csv`).<br>

### 2. `/tone/`<br>

Retrieves the tones (sentiment) of GDELT events based on the provided filters.

**Parameters:**<br>
- `keyword` (str): The keyword to search for in the events.<br>
- `start_date` (str): The start date for the event search (YYYY-MM-DD format).<br>
- `end_date` (str): The end date for the event search (YYYY-MM-DD format).<br>
- `country` (str): The country or list of countries to filter the events by.<br>

**Response:**<br>
- Returns a pandas DataFrame containing the retrieved event tones.<br>
- The DataFrame is also saved as a CSV file (e.g., `csv_tono_1.csv`).<br>

### 3. `/popularity/`

Retrieves the popularity information of GDELT events based on the provided filters.<br>

**Parameters:**<br>
- `keyword` (str): The keyword to search for in the events.<br>
- `start_date` (str): The start date for the event search (YYYY-MM-DD format).<br>
- `end_date` (str): The end date for the event search (YYYY-MM-DD format).<br>
- `country` (str): The country or list of countries to filter the events by.<br>

**Response:**
- Returns a pandas DataFrame containing the retrieved event popularity information.<br>
- As before, the DataFrame is also saved as a CSV file (e.g., `csv_popularidad_1.csv`).<br>

### 4. `/limpieza/`

Cleans the data retrieved from the other endpoints by removing null values and duplicates.<br>

**Parameters:**<br>
- `funcion_obtener_datos` (str): The name of the function used to retrieve the data ("articles", "tone", or "popularity").<br>

- `keyword` (str): The keyword used in the original data retrieval.<br>

- `start_date` (str): The start date used in the original data retrieval (YYYY-MM-DD format).

- `end_date` (str): The end date used in the original data retrieval (YYYY-MM-DD format).<br>

- `country` (str): The country or list of countries used in the original data retrieval.<br>

**Response:**

- Returns a message indicating that the data has been cleaned and saved to a CSV file.<br>

- The cleaned DataFrame is saved as a CSV file (e.g., `csv_articles_limpios_1.csv`).<br>

## Usage

1. Install requiremnts.<br>

2. Run the FastAPI application.

3. Use the provided endpoints to retrieve and process GDELT data based on your requirements.

