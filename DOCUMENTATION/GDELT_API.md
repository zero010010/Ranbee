
# FastAPI Application for GDELT Data Extraction

This FastAPI application provides endpoints to extract daily, monthly, and quarterly data from the GDELT (Global Database of Events, Language, and Tone) database based on specified filters. It also includes an endpoint for cleaning the data, an endpoint for extracting data for a specific proyect, for example including all countries in a determined list. 

## Endpoints

### `/diary/extraction`

This endpoint allows you to extract daily data from GDELT based on the provided parameters.

#### Parameters

- `funcion_obtener_datos` (str): The function to use for data extraction. Accepted values are `"tone"` and `"popularity"`.
- `keyword` (str): The keyword to filter the data.
- `country` (str): The country code to filter the data.
- `descarga` (str): Specify `"yes"` to save the extracted data as a CSV file.

#### Response

The endpoint returns a Pandas DataFrame containing the extracted data. If `descarga` is set to `"yes"`, the data will also be saved as a CSV file in the `data_diario` directory, organized by the `funcion_obtener_datos` and `country` parameters.

### `/monthly/extraction`

This endpoint allows you to extract monthly data from GDELT based on the provided parameters.

#### Parameters

- `funcion_obtener_datos` (str): The function to use for data extraction. Accepted values are `"tone"` and `"popularity"`.
- `keyword` (str): The keyword to filter the data.
- `country` (str): The country code to filter the data.

#### Response

The endpoint returns a message indicating the successful download of the monthly data. The data is saved as a CSV file in the `data_mensual` directory, organized by the `funcion_obtener_datos` and `country` parameters.

### `/quaterly/extraction`

This endpoint allows you to extract quarterly data from GDELT based on the provided parameters.

#### Parameters

- `funcion_obtener_datos` (str): The function to use for data extraction. Accepted values are `"tone"` and `"popularity"`.
- `keyword` (str): The keyword to filter the data.
- `country` (str): The country code to filter the data.

#### Response

The endpoint returns a message indicating the successful download of the quarterly data. The data is saved as a CSV file in the `data_trimestral` directory, organized by the `funcion_obtener_datos` and `country` parameters.

### `/clean`

This endpoint allows you to clean the extracted data based on the provided parameters.

#### Parameters

- `funcion_obtener_datos` (str): The function to use for data extraction. Accepted values are `"tone"` and `"popularity"`.
- `keyword` (str): The keyword to filter the data.
- `country` (str): The country code to filter the data.
- `periodo` (str): The time period for cleaning the data. Accepted values are `"diary"`, `"monthly"`, and `"quaterly"`.

#### Response

The endpoint returns a message indicating the successful cleaning of the data. The cleaned data is saved as a CSV file in the `data_limpio` directory, organized by the `funcion_obtener_datos`, `periodo`, and `country` parameters.

### `/project`

This endpoint allows you to extract data for a specific project, eg: including all countries in a predefined list.

#### Parameters

- `funcion_obtener_datos` (str): The function to use for data extraction. Accepted values are `"tone"` and `"popularity"`.
- `keyword` (str): The keyword to filter the data.
- `periodo` (str): The time period for extracting the data. Accepted values are `"monthly"` and `"quaterly"`.

#### Response

The endpoint returns a message indicating the successful download of the data for all countries. The data is saved as CSV files in the `data_final` directory, organized by the `funcion_obtener_datos`, `periodo`, and `keyword` parameters.

