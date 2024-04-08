# Import required libraries
from fastapi import FastAPI
import pandas as pd
import os
import requests
import gzip
import json
from util.funcionesEurostat import encontrar_dfs_con_valores_cero, encontrar_dfs_vacios, salvar_df_processed, salvar_dfs_preprocessed, generar_serie_suma, completar_series_trimestrales

# Create a FastAPI instance
app = FastAPI()

# 1 ENDPOINT FOR EXTRACTING EUROSTAT DATA AND 2 FOR VISUALIZING PART OF THE DATA

# Define a GET endpoint for setting up the API
@app.get("/eurostat/")
def setup_api():
    # URL for the Eurostat API endpoint
    url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/lfsq_pganws/?format=SDMX-CSV&compressed=true"

    # Send a GET request to the URL
    response = requests.get(url)

    # Open a file and write the response content
    with open('estat_lfsq_pganws_en.csv', 'wb') as f:
        f.write(response.content)
    archivo_comprimido = 'estat_lfsq_pganws_en.csv'
    nombre_descomprimido = 'estat_lfsq_pganws-decodificado.csv'  # Change 'nombre_del_archivo.tsv' to the desired name for the decompressed file

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
    df = df.drop(['DATAFLOW', 'freq', 'unit', 'OBS_FLAG', 'LAST UPDATE'], axis=1)
    # Fill NaN values with zero
    df['OBS_VALUE'] = df['OBS_VALUE'].fillna(0)
    df['OBS_VALUE'] = df['OBS_VALUE'].round(1)

    # Function to map quarters to specific months
    def map_quarter_to_month(quarter):
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
    df_foreigners_act = df[(df['citizen'] == 'FOR') & (df['wstatus'] == 'ACT')]
    # Filter for dates after 2014
    df_foreigners_act = df_foreigners_act[df_foreigners_act['year_month'] >= '2017-01-01']

    # List of countries
    countries = ['AT', 'BE', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EL', 'ES',
                 'FI', 'FR', 'IE', 'IT', 'LU', 'NL', 'NO