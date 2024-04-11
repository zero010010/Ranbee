from fastapi import FastAPI 
import pandas as pd
import os
import requests
import gzip
import json
from util.funcionesEurostat import encontrar_dfs_con_valores_cero,encontrar_dfs_vacios,salvar_df_processed,salvar_dfs_preprocessed,generar_serie_suma,completar_series_trimestrales


app = FastAPI()

# ENDPOINT FOR EXTRACTING EUROSTAT DATA AND 2 FOR VISUALIZING PART OF THE DATA

@app.get("/eurostat/") 

def fetch_eurostat_data():
    """
    Fetches Eurostat data from the API, 
    decompresses the downloaded file, 
    and saves the data to a CSV file in the "data/raw" directory.

    Sends GET request to the Eurostat API endpoint to download a compressed CSV file 
    then decompresses the file and saves the decompressed data to a new CSV file.
      cleans and preprocesses the data by dropping unnecessary columns and filling NaN values with zeros.
    """
def setup_api():
  # URL for the Eurostat API endpoint
  url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/lfsq_pganws/?format=SDMX-CSV&compressed=true"
  # Send a GET request to the URL
  response = requests.get(url)
  # Open a file and write the response content
  with open('estat_lfsq_pganws_en.csv', 'wb') as f:
      f.write(response.content)
  archivo_comprimido = 'estat_lfsq_pganws_en.csv' 
  nombre_descomprimido = 'estat_lfsq_pganws-decodificado.csv'  # Change name to 'estat_lfsq_pganws-decodificado.csv'
  # Decompress the compressed file
  with gzip.open(archivo_comprimido, 'rb') as f:
    datos_descomprimidos = f.read()

  # Save the decompressed data to a file
  with open(nombre_descomprimido, 'wb') as f:
    f.write(datos_descomprimidos)

  # Read the decompressed CSV file
  df = pd.read_csv("estat_lfsq_pganws-decodificado.csv")

  # Check if the output folder exists, if not, create it
  if not os.path.exists("data/raw"):
    os.makedirs("data/raw")
  df.to_csv('data/raw/eurostat.csv')
  # Clean and preprocess the data
  df = df.drop(['DATAFLOW','freq','unit','OBS_FLAG','LAST UPDATE'],axis=1)
  # Fill NaN values with zero
  df['OBS_VALUE'] = df['OBS_VALUE'].fillna(0)
  df['OBS_VALUE'] = df['OBS_VALUE'].round(1)


    
def map_quarter_to_month(quarter):
     """
    Converts a quarter string to month string in the format 'YYYY-MM-01'.
    
    Args:
        quarter (str): A string representing a quarter in the format 'YYYY-Qn', 
        where YYYY is the year and n is the quarter number (1-4).
    
    Returns:
        str: A string representing the first day of the corresponding month in the format 'YYYY-MM-01',
          or None if the input is invalid.
    """
     year, q = quarter.split('-Q')
     if q == '1':
        return f"{year}-03-01"
     elif q == '2':
        return f"{year}-06-01"
     elif q == '3':
        return f"{year}-09-01"
     elif q == '4':
        return f"{year}-12-01"
     else:
        return None

  
# Create a new column 'year_month' based on the 'TIME_PERIOD' column
  df['year_month'] = df['TIME_PERIOD'].apply(map_quarter_to_month)

  # Apply filters for foreigners and active status
  df_foreigners_act = df[(df['citizen']=='FOR') & (df['wstatus']=='ACT')]
  # Filter after 2014
  df_foreigners_act = df_foreigners_act[df_foreigners_act['year_month'] >= '2017-01-01']

  # List of countries
  countries = ['AT', 'BE', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EL', 'ES',
       'FI', 'FR', 'IE', 'IT', 'LU', 'NL', 'NO', 'PT', 'SE', 'SI', 'TR']

  # Create a dictionary of DataFrames, one for each country,one for males and one for females
  dfs_by_country = {}
  for country in countries:
    dfs_by_country[country] = [df_foreigners_act[(df_foreigners_act['geo'] == country) & (df_foreigners_act['sex'] == 'M')],
                               df_foreigners_act[(df_foreigners_act['geo'] == country) & (df_foreigners_act['sex'] == 'F')]]

  # Create a list to store countries with empty DataFrames and remove them
  for pais in paises_con_dfs_vacios:
    del dfs_by_country[pais]

  # Iterarate over the dicctionary 
  for country, dfs in dfs_by_country.items():
    # Iterate over the dataframes for current countries
    for df_gender in dfs:
        # Calculate total observations per date 
        df_gender['total_obs_value'] = df_gender.groupby('year_month')['OBS_VALUE'].transform('sum')
        df_gender['total_obs_value'] = df_gender['total_obs_value'].round(1)

  # Create a list to store DataFrames with 50% or more zero values and remove them
  lista = encontrar_dfs_con_valores_cero(dfs_by_country)
  #print(lista)
  for i in lista:
    del dfs_by_country[i]

  # Save the preprocessed data in the 'preprocessed' folder
  salvar_dfs_preprocessed(dfs_by_country)

  # Save the processed data in the 'processed' folder
  salvar_df_processed(dfs_by_country)

  
  completar_series_trimestrales('data/processed')

  # Generate the EU summary serie
  generar_serie_suma('data/processed')
  return ("setup completo")# Return a success message

@app.get("/eurostat/head")# Define a GET endpoint to display the head of the raw Eurostat data

def head():
    """
    Retrieves the first 5 rows of the Eurostat data
    returns: JSON.

    Returns:
        dict: A JSON-serialized dictionary containing the first 5 rows of the Eurostat data.
    """


def head_api():
    
    
    df = pd.read_csv("data/raw/eurostat.csv")
    df_ = df.head(5)
    # Convert the DataFrame to JSON and return it
    return json.loads(df_.to_json(orient='records'))

@app.get("/eurostat/serie")#GET endpoint to display the head of the EU summary series

def serie_api():
    
    df = pd.read_csv("data/serie/serie_EU.csv")
    df_ = df.head(5)
    return json.loads(df_.to_json(orient='records'))



@app.get("/eda")

@app.get("/eda")
def eda():
    '''New endpoint @app.eda
    From the endpoints @app.get("/eurostat/") and @app.get("/eurostat/serie")
    Performs Exploratory Data Analysis (EDA)
    and saves the results in a CSV file
    inside the "EDA" folder'''
    



def perform_eda(data_source: str):
    """
(EDA) on the Eurostat or EU summary series data, 
saves the results to a CSV file.

Args:
    data_source (str): source to perform EDA on. "eurostat" or "serie".

Returns:
    dict: A dictionary containing a message indicating the path for the EDA results file.
"""
    # # Verify the value of data_source and get the corresponding DataFrame
    if data_source == "eurostat":
        df = pd.read_csv("data/raw/eurostat.csv")  #  endpoint "/eurostat/"
    elif data_source == "serie":
        df = pd.read_csv("data/serie/serie_EU.csv")  # endpoint "/eurostat/serie"
    else:
        # If data_source is invalid, return an error
        return {"error": "Invalid data source"}

    # EDA
    eda_results = {
        "num_rows": len(df),  # number of rows
        "num_columns": len(df.columns),  # number of columns
        "column_names": list(df.columns),  # list of column names
        "null_counts": df.isnull().sum().to_dict(),  # counts of null values por columna
        "data_types": df.dtypes.to_dict(),  # data types of each column
        "descriptive_stats": df.describe().to_dict()  # descriptive stats 
    }

    # Create the "EDA" folder if it doesn't exist
    eda_folder = "EDA"
    if not os.path.exists(eda_folder):
        os.makedirs(eda_folder)

    # Generate a unique filename to save the EDA results
     
    filename = f"{eda_folder}/eda_{data_source}.csv"

    # Save the EDA results to a CSV 
    eda_df = pd.DataFrame.from_dict(eda_results, orient="index")
    eda_df.to_csv(filename)

    # Return a message indicating the path of the saved file
    return {"message": f"EDA results for {data_source} saved to {filename}"}

