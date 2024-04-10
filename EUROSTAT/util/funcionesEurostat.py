import pandas as pd
import os
from datetime import datetime

def encontrar_dfs_vacios(dfs_by_country):
    """
    Devuelve los paises con dataframes vacios.
    
    Parámetros:
        dfs_by_country (dic): dccionario con dos dfs por pais, uno masculino y otro femenino.
        

    Retorna: paises_con_dfs_vacios (lista) : claves de paises con dfs vacios. 
   """
    # Crear una lista para almacenar los países con DataFrames vacíos
    paises_con_dfs_vacios = []

    # Iterar sobre el diccionario
    for country, dfs in dfs_by_country.items():
        # Verificar si ambas listas están vacías
        if len(dfs[0]) == 0 and len(dfs[1]) == 0:
            paises_con_dfs_vacios.append(country)
    
    return paises_con_dfs_vacios


def salvar_dfs_preprocessed(dfs_by_country):
    """
    Guardan 2 csv por pais, uno con observaciones masculinas y otro femeninas.

    Parámetros:
        dfs_by_country (dic): dccionario con dos dfs por pais, uno masculino y otro femenino.
        

    Retorna: None
   """
    if not os.path.exists("data/pre-processed"):
        os.makedirs("data/pre-processed")

    # Iterar sobre las claves y valores del diccionario
    for pais, dfs_pais in dfs_by_country.items():
        i = 0
        for df in dfs_pais:
            # Generar el nombre del archivo CSV
            if (i == 0):
                nombre_archivo = f"data/pre-processed/foreigner_act_{pais}_M.csv"
                i = 1
            else:
            
                nombre_archivo = f"data/pre-processed/foreigner_act_{pais}_F.csv"
        # Guardar el DataFrame como un archivo CSV
        df.to_csv(nombre_archivo, index=False)


def salvar_df_processed(dfs_by_country):
    
    """
    Guarda una serie por pais con las observaciones masculinas y totales para ese pais.

    Parámetros:
        dfs_by_country (dic): dccionario con dos dfs por pais, uno masculino y otro femenino.
        

    Retorna: None
   """
        
    if not os.path.exists("data/processed"):
        os.makedirs("data/processed")

    # Iterar sobre las claves y valores del diccionario
    for pais, dfs_pais in dfs_by_country.items():
        df1 = dfs_pais[0]
        df1.reset_index(drop=True, inplace=True)
        df2 = dfs_pais[1]
        df2.reset_index(drop=True, inplace=True) 
        df1['year_month'] = pd.to_datetime(df1['year_month'])
        df2['year_month'] = pd.to_datetime(df2['year_month'])
    
        # Encontrar la fecha mínima común entre los dos DataFrames
        fecha_minima_comun = max(df1['year_month'].min(), df2['year_month'].min())
        fecha_maxima_comun = min(df1['year_month'].max(), df2['year_month'].max())
    
        # Seleccionar el rango de filas basado en la fecha mínima común
        nuevo_df1 = df1[df1['year_month'] >= fecha_minima_comun].reset_index(drop=True)
        nuevo_df2 = df2[df2['year_month'] >= fecha_minima_comun].reset_index(drop=True)
    
        # Calcular la suma de las últimas columnas de df1 y df2
        suma_ultimas_columnas = nuevo_df1.iloc[:, -1] + nuevo_df2.iloc[:, -1]
    
        # Añadir la serie resultante como una nueva columna llamada 'total' a df1
        nuevo_df1['total'] = suma_ultimas_columnas.round(1)
        #nuevo_df1 = nuevo_df1.drop_duplicates(subset=['year_month'])
        nombre_archivo = f"data/processed/foreigners_act_{pais}_MyF.csv"
        indice_fecha_maxima = nuevo_df1['year_month'].idxmax()

        res = nuevo_df1.iloc[:indice_fecha_maxima+1,7:]    
        # Guardar el DataFrame como un archivo CSV
        res.to_csv(nombre_archivo, index=False)

def encontrar_dfs_con_valores_cero(dfs_by_country):
    """
    Encuentra los df con mas del 50% de valores cero.

    Parámetros:
        dfs_by_country (dic): dccionario con dos dfs por pais, uno masculino y otro femenino.
        

    Retorna: key_to_delete (lista): lista de claves de pais con aquellos que cumplen la condicion
   """
       
    # Lista para almacenar las claves de los DataFrames que se eliminarán
    keys_to_delete = []
    
    # Crear una copia de las claves del diccionario
    keys_copy = list(dfs_by_country.keys())
    
    # Iterar sobre las claves del diccionario
    for country in keys_copy:
        dfs_pais = dfs_by_country[country]
        for i, df in enumerate(dfs_pais):
            # Calcular el porcentaje de valores cero en 'total_obs_value'
            porcentaje_ceros = (df['total_obs_value'] == 0).mean() * 100
            
            # Verificar si el porcentaje de ceros es mayor al 50%
            if porcentaje_ceros > 50:
                # Agregar la clave del DataFrame a la lista de claves a eliminar
                keys_to_delete.append(country)
                break
    
        
    return keys_to_delete

def completar_series_trimestrales(ruta_carpeta):
    """
    Completa series temporales trimestrales faltantes en archivos CSV ubicados en un directorio
    de entrada y guarda las series completas en otro directorio.

    Parámetros:
        ruta_carpeta (str): La ruta al directorio que contiene los archivos CSV de series temporales.
        
    Retorna: None
   """
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists("data/series"):
        os.makedirs("data/series")
    
    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(ruta_carpeta)
    
    # Iterar sobre los archivos en la carpeta
    for archivo in archivos:
        # Verificar que el archivo es un archivo CSV
        if archivo.endswith('.csv'):
            # Construir la ruta completa al archivo
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            # Leer el archivo CSV
            df = pd.read_csv(ruta_archivo)
            # Convertir la columna 'year_month' a tipo datetime
            df['year_month'] = pd.to_datetime(df['year_month'])
            # Eliminar filas duplicadas si existen
            df = df.drop_duplicates(subset=['year_month'])
            # Obtener la menor y la mayor fecha presente en el DataFrame
            min_fecha = df['year_month'].min()
            max_fecha = df['year_month'].max()
            # Crear una serie temporal mensual entre la menor y la mayor fecha
            fechas_mensuales = pd.date_range(start=min_fecha, end=max_fecha, freq='Q')
            # Crear un DataFrame vacío con las fechas mensuales como índice
            df_mensual = pd.DataFrame(index=fechas_mensuales)
            # Rellenar la serie temporal mensual con los valores del trimestre correspondiente
            df_mensual['total'] = df.set_index('year_month').resample('Q').ffill()['total']
            # Guardar el DataFrame reducido como un archivo CSV
            ruta_nueva = os.path.join("data/series", archivo)
            df_mensual.to_csv(ruta_nueva)

def generar_serie_suma(directorio_entrada):
    """
    Genera una serie con la suma de todas las series en archivos CSV ubicados en un directorio de entrada y guarda la serie resultante en un archivo CSV.

    Parámetros:
        directorio_entrada (str): La ruta al directorio que contiene los archivos CSV de las series a sumar.
        archivo_salida (str): La ruta al archivo CSV donde se guardará la serie resultante.

    Retorna: None
    """
    
    # Leer los archivos en el directorio de entrada
    archivos = os.listdir(directorio_entrada)
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists("data/serie"):
        os.makedirs("data/serie")

    # Inicializar una lista para almacenar las series individuales
    series = []

    # Leer los archivos en el directorio de entrada
    archivos = os.listdir(directorio_entrada)

    # Encontrar la serie con el mayor rango de fechas
    fechas_maximas = pd.Series()
    for archivo in archivos:
        if archivo.endswith('.csv'):
            ruta_archivo = os.path.join(directorio_entrada, archivo)
            df = pd.read_csv(ruta_archivo, index_col=0)
            
            # Encontrar las fechas únicas de esta serie y actualizar fechas_maximas si es necesario
            fechas_actuales = pd.Series(df.index.unique())
            if len(fechas_actuales) > len(fechas_maximas):
                fechas_maximas = fechas_actuales

    # Crear una serie con todas las fechas y total igual a cero
    serie_vacia = pd.DataFrame(index=fechas_maximas, data={'total': 0})

    # Sumar una a una las series temporales de cada país
    for archivo in archivos:
        if archivo.endswith('.csv'):
            ruta_archivo = os.path.join(directorio_entrada, archivo)
            df = pd.read_csv(ruta_archivo, index_col=0)
            
            # Sumar la serie al DataFrame de la serie resultante
            serie_vacia = serie_vacia.add(df, fill_value=0)

    # Guardar la serie resultante en un archivo CSV
    serie_vacia = serie_vacia['total']
    serie_vacia.to_csv('data/serie/serie_EU.csv')
