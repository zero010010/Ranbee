from fastapi import FastAPI
import pandas as pd
import os
import requests
import gzip
import json
from util.funcionesEurostat import encontrar_dfs_con_valores_cero,encontrar_dfs_vacios,salvar_df_processed,salvar_dfs_preprocessed,generar_serie_suma,completar_series_trimestrales


app = FastAPI()

# # 1 ENDPOINT FOR EXTRACTING EUROSTAT DATA AND 2 FOR VISUALIZING PART OF THE DATA

@app.get("/eurostat/") 
def setup_api():
  url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/lfsq_pganws/?format=SDMX-CSV&compressed=true"

  response = requests.get(url)

  with open('estat_lfsq_pganws_en.csv', 'wb') as f:
      f.write(response.content)
  archivo_comprimido = 'estat_lfsq_pganws_en.csv' 
  nombre_descomprimido = 'estat_lfsq_pganws-decodificado.csv'  # Cambia 'nombre_del_archivo.tsv' al nombre deseado para el archivo descomprimido

  with gzip.open(archivo_comprimido, 'rb') as f:
    datos_descomprimidos = f.read()

  # Guardar los datos descomprimidos en un archivo
  with open(nombre_descomprimido, 'wb') as f:
    f.write(datos_descomprimidos)

  # LECTURA FICHERO DESCOMPRIMIDO
  df = pd.read_csv("estat_lfsq_pganws-decodificado.csv")

  # Verificar si la carpeta de salida existe, si no, crearla
  if not os.path.exists("data/raw"):
    os.makedirs("data/raw")
  df.to_csv('data/raw/eurostat.csv')
  # LIMPIEZA Y TRATAMIENTO
  df = df.drop(['DATAFLOW','freq','unit','OBS_FLAG','LAST UPDATE'],axis=1)
  # rellena valores nan por cero
  df['OBS_VALUE'] = df['OBS_VALUE'].fillna(0)
  df['OBS_VALUE'] = df['OBS_VALUE'].round(1)

  # Función para mapear los trimestres a meses específicos
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

  # Crear la nueva columna 'year_month' basada en la columna 'TIME_PERIOD'
  df['year_month'] = df['TIME_PERIOD'].apply(map_quarter_to_month)

  # APLICAMOS FILTROS DE EXTRANJEROS, ACTIVOS
  df_foreigners_act = df[(df['citizen']=='FOR') & (df['wstatus']=='ACT')]
  # Fecha superior a 2014
  df_foreigners_act = df_foreigners_act[df_foreigners_act['year_month'] >= '2017-01-01']

  # paises
  countries = ['AT', 'BE', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EL', 'ES',
       'FI', 'FR', 'IE', 'IT', 'LU', 'NL', 'NO', 'PT', 'SE', 'SI', 'TR']

  # Crear un diccionario de DataFrames, uno por cada país
  dfs_by_country = {}
  for country in countries:
    dfs_by_country[country] = [df_foreigners_act[(df_foreigners_act['geo'] == country) & (df_foreigners_act['sex'] == 'M')],
                               df_foreigners_act[(df_foreigners_act['geo'] == country) & (df_foreigners_act['sex'] == 'F')]]

  # Crear una lista para almacenar los países con DataFrames vacíos y los elimina
  paises_con_dfs_vacios = encontrar_dfs_vacios(dfs_by_country)
  for pais in paises_con_dfs_vacios:
    del dfs_by_country[pais]

  # Iterar sobre el diccionario
  for country, dfs in dfs_by_country.items():
    # Iterar sobre los DataFrames para el país actual
    for df_gender in dfs:
        # Calcular el total de observaciones por fecha
        df_gender['total_obs_value'] = df_gender.groupby('year_month')['OBS_VALUE'].transform('sum')
        df_gender['total_obs_value'] = df_gender['total_obs_value'].round(1)

  # Crear una lista para almacenar los DataFrames con 50% vacíos y los elimina
  lista = encontrar_dfs_con_valores_cero(dfs_by_country)
  #print(lista)
  for i in lista:
    del dfs_by_country[i]

  # SALVA EN PRE-PROCESSED
  salvar_dfs_preprocessed(dfs_by_country)

  # SALVA EN PROCESSED
  salvar_df_processed(dfs_by_country)

  # COMPLETA LAS SERIES
  completar_series_trimestrales('data/processed')

  # GENERA LA SERIE EU
  generar_serie_suma('data/processed')
  return ("setup completo")

@app.get("/eurostat/head")
def head_api():
    """
    Función muestra el head
    """
    df = pd.read_csv("data/raw/eurostat.csv")
    df_ = df.head(5)
    return json.loads(df_.to_json(orient='records'))

@app.get("/eurostat/serie")
def serie_api():
    """
    Función muestra el head
    """
    df = pd.read_csv("data/serie/serie_EU.csv")
    df_ = df.head(5)
    return json.loads(df_.to_json(orient='records'))
