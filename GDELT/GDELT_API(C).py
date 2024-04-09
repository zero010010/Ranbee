# importing libraries
from fastapi import FastAPI
from gdeltdoc import GdeltDoc, Filters
import pandas as pd
import os
import datetime
import time


#  Initializes FastAPI.

app = FastAPI()

# Defines a GET endpoint for downloading daily data. (Note: Maximum number of countries allowed 9)
@app.get("/diary/extraction") 
# Function to download daily data, arg : data type, keyword, country, download option   
def descargar_datos_diarios(funcion_obtener_datos: str, keyword: str, country: str,descarga: str):   
    f = Filters(keyword=keyword, 
                    start_date="2017-01-01",
                    end_date="2023-12-31",
                    country=country)
    gd = GdeltDoc() # Initialize GdeltDoc class 
    if funcion_obtener_datos.lower() == "tone":
        results = gd.timeline_search("timelinetone", f)
        df = pd.DataFrame(results) # Converts results to DataFrame
    elif funcion_obtener_datos.lower() == "popularity":# Checks if popularity is specified
        results = gd.timeline_search("timelinevol", f) # Calls timeline_search method based on filter
        df = pd.DataFrame(results)# Results to DataFrame

    else:
        return "Error: La función de extracción de datos especificada no es válida."

    if descarga.lower() == "yes": # Check if download option is yes
        carpeta_padre = "data_diario" # creat parent folder 
        if not os.path.exists(carpeta_padre):# Check if parent folder exists
            os.makedirs(carpeta_padre)# If not, create it
    
        carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}" # Create subfolder route based on data type
        if not os.path.exists(carpeta_tipo_datos):
            os.makedirs(carpeta_tipo_datos)
    
        # Check if file with same name already exists, if so, increment file number 
        file_number = 1
        while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):
            file_number += 1
        filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_diarios_{file_number}.csv"
        df.to_csv(filename, index=False)# Save DataFrame to CSV file
    
    return df


@app.get("/monthly/extraction") # Defines a GET endpoint for downloading monthly data for countries
def descargar_datos_mensuales(funcion_obtener_datos: str, keyword: str, country: str):
    if funcion_obtener_datos == "tone":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no") # function avoids downloading again
        df['datetime'] = pd.to_datetime(df['datetime'])# convert datetime column to datetime
        
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()# group by month and sum values
    elif funcion_obtener_datos == "popularity":# 
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country,"no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index() # group by month and sum values

    else:
        return {"mensaje": "Función de obtener datos no válida"}

    carpeta_padre = "data_mensual" # creat parent folder
    if not os.path.exists(carpeta_padre): # Check if parent folder exists, if not create it
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}" # Create subfolder route based on data type
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # create csv file path
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_mensual_{file_number}.csv"
    df_monthly.to_csv(filename, index=False)# Save DataFrame to CSV file
    
    return f"Data of {funcion_obtener_datos.capitalize()} downloaded successfully"

@app.get("/quaterly/extraction") # Defines a GET endpoint for downloading quarterly data
def descargar_datos_trimestrales(funcion_obtener_datos: str, keyword: str, country: str):# Function to download quarterly data, arg : data type, keyword, country
    if funcion_obtener_datos == "tone":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        # groupby quarter and sum values
        df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
    elif funcion_obtener_datos == "popularity":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() 
    else:
        return {"mensaje": "Función de obtener datos no válida"}

    carpeta_padre = "data_trimestral" # creat parent folder 
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}" #  Create subfolder route
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # csv file path 
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"
    df_quaterly.to_csv(filename, index=False)# Save DataFrame to CSV file
    
    return f"Data of {funcion_obtener_datos.capitalize()} downloaded successfully"

#  Defines a GET endpoint cleaning data 
def limpiar_dataframe(df: pd.DataFrame,freq:str): # function to clean dataframe, arg : dataframe, frequency
    # Convert datetime column to datetime type, it fills missing dates with 0
    start_date = df['datetime'].min()
    end_date = df['datetime'].max()
    all_dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    df = df.set_index('datetime').reindex(all_dates).fillna(0).reset_index()# fill missing dates with 0
    df = df.rename(columns={'index': 'datetime'}) # rename datetime column as datetime
    df_limpio= df.dropna().drop_duplicates()# drop na and duplicate values
    return df_limpio 


# Cleaning 
@app.get("/clean")
def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, country: str,periodo:str): # function to clean dataframe, arg : data type, keyword, country, period
    if funcion_obtener_datos.lower() == "tone":
        results = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")# 
        df = pd.DataFrame(results)# Convert results to DataFrame
        folder_name = "tone"# Set folder name
    elif funcion_obtener_datos.lower() == "popularity":
        results = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df = pd.DataFrame(results)
        folder_name = "popularity" 
    else:
        return "Error: La función de extracción de datos especificada no es válida."
        
    if periodo.lower() == "monthly":
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
        save_folder = f"./data_limpio/{folder_name}/monthly"
        df_save = df_monthly
        df_save = limpiar_dataframe(df_save, "M") # Monthly data cleaning
    elif periodo.lower() == "diary":
        save_folder = f"./data_limpio/{folder_name}/diary"
        df_save = limpiar_dataframe(df,"D")
    elif periodo.lower() == "quaterly":
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() # group by quarter and sum values
        save_folder = f"./data_limpio/{folder_name}/quaterly"
        df_save = df_trimestral
        df_save = limpiar_dataframe(df_save,"Q") # clean quarterly data
            
    else:
        return "Error: El intervalo especificado no es válido."
        
    os.makedirs(save_folder, exist_ok=True) # create folder if not exists

    # save cleaned dataframe to csv file
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # avoid re-writing existing files by adding timestamp to filename
    filename = f"{save_folder}/{keyword}_limpio_{folder_name}_{periodo}_{country}_{file_timestamp}.csv"  # Agregar el nombre del país y el periodo de tiempo al archivo CSV
    df_save.to_csv(filename, index=False)
    
    return f"Dates of {funcion_obtener_datos.capitalize()} has been cleaned successfully"

# Sample : endpoint_limpiar_dataframe("articles","Unemployement Benefits","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"])

@app.get("/project") # download data for all countries for given keyword and period
def extraccion_total(funcion_obtener_datos: str, keyword: str, periodo: str):# function to download data for all countries, arg : data type, keyword, period
    """
    Extracts data for all countries for a given keyword and time period.
    
    Args:
        funcion_obtener_datos (str): The type of data to extract, either "tone" or "popularity".
        keyword (str): The keyword to search for.
        periodo (str): The time period to extract data for, either "monthly" or "quaterly".
    
    Returns:
        str: A message indicating that the data has been downloaded successfully.
    """

    countries = ['Austria', 'Belgium', 'Switzerland', 'Cyprus', 'EZ', 'Germany', 'Denmark', 'Greece', 'Spain', 'Finland', 'France', 'Ireland', 'Italy', 'Luxembourg', 'Netherlands', 'Norway', 'Portugal', 'Sweden', 'Slovenia']
    for country in countries:
        f = Filters(keyword=keyword, # loop through countries list
                    start_date="2017-01-01",
                    end_date="2023-12-31",
                    country=country)
        gd = GdeltDoc() 
        
        if funcion_obtener_datos.lower() == "tone":
            results = gd.timeline_search("timelinetone", f)
            df = pd.DataFrame(results)
            folder_name = "tone"
        elif funcion_obtener_datos.lower() == "popularity":
            results = gd.timeline_search("timelinevol", f)
            df = pd.DataFrame(results)
            folder_name = "popularity"
        else:
            return "Error: La función de extracción de datos especificada no es válida."
        
        if periodo.lower() == "monthly":
            df['datetime'] = pd.to_datetime(df['datetime'])
            df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
            save_folder = f"./data_final/{folder_name}/monthly/{keyword}"
            df_save = df_monthly
            df_save = limpiar_dataframe(df_save, "M") # monthly data cleaning
        elif periodo.lower() == "quaterly":
            df['datetime'] = pd.to_datetime(df['datetime'])
            df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() 
            save_folder = f"./data_final/{folder_name}/quaterly/{keyword}"
            df_save = df_trimestral
            df_save = limpiar_dataframe(df_save,"Q") # quartely data cleaning   
            
        else:
            return "Error: El intervalo especificado no es válido."
        
        os.makedirs(save_folder, exist_ok=True) # create folder if not exists

        # y guardamos
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # avoid re-writing existing files by adding timestamp to filename
        filename = f"{save_folder}/{keyword}_{folder_name}_{periodo}_{country}_{file_timestamp}.csv"  # Agregate country name and time period to csv filename
        df_save.to_csv(filename, index=False)# save cleaned dataframe to csv file with timestamp in filename
    
    return f"Mean of {funcion_obtener_datos.capitalize()} data downloaded successfully for all countries"

# OPTIONAL, PENDING REVIEW
@app.get("/mean")# calculate mean of column for all csvs in folder
def calcular_media(csv_folder, column_name,output_csv: bool = False): 
    """
    Calculates the mean of a specified column across all CSV files in a directory.
    
    Args:
        csv_folder (str): The path to the directory containing the CSV files.
        column_name (str): The name of the column to calculate the mean for.
        output_csv (bool, optional): If True, the mean values will be saved to a CSV file in the parent directory of `csv_folder`. Defaults to False.
    
    Returns:
        pd.DataFrame: A DataFrame containing the mean values for the specified column.
    """
    dfs = []# create empty list to store dataframes
    for filename in os.listdir(csv_folder):# loop through files in folder
        if filename.endswith(".csv"):# only process csv files
            file_path = os.path.join(csv_folder, filename)# construct file path
            df = pd.read_csv(file_path, parse_dates=['datetime'])# read csv file into dataframe
            print(f"Leyendo archivo: {file_path}")# print file being processed
            if column_name in df.columns:# check if column exists in file
                df.set_index('datetime', inplace=True)# set datetime as index
                dfs.append(df[column_name].rename(filename.split('.')[0]))  # Rename series and append to list
            else:
                print(f"La columna '{column_name}' no se encontró en el archivo: {file_path}")

    if not dfs:
        print(f"No se encontraron archivos CSV en el directorio: {csv_folder}")
        return pd.DataFrame()

    combined_df = pd.concat(dfs, axis=1)# concat dfs into single dataframe
    media_columna = combined_df.mean(axis=1)  # calculate mean across rows
    media_df = pd.DataFrame({column_name: media_columna}) # create dataframe with mean column
    if output_csv:
        parent_directory = os.path.dirname(csv_folder)# get parent directory of csv folder
        output_path = os.path.join(parent_directory, f"media_{column_name}.csv")# construct output path
        media_df.to_csv(output_path, index=False)# 
        return {"message": f"Archivo CSV guardado en: {output_path}"}
    else:
        return media_df

@app.get("/total_mean/") # obtain total mean across all csvs
def total_mean():
# folder routes
    tono_mensual_csv_folder = "./data_final/tone/monthly"
    popularity_mensual_csv_folder = "./data_final/popularity/monthly"
    tono_trimestral_csv_folder = "./data_final/tone/quaterly"
    popularity_trimestral_csv_folder = "./data_final/popularity/quaterly"

    # mean tone / popularity monthly and quaterly   
    media_tono_mensual = calcular_media(tono_mensual_csv_folder, 'Average Tone')
    media_popularity_mensual = calcular_media(popularity_mensual_csv_folder, 'Volume Intensity')
    media_tono_trimestral = calcular_media(tono_trimestral_csv_folder, 'Average Tone')
    media_popularity_trimestral = calcular_media(popularity_trimestral_csv_folder, 'Volume Intensity')

    # Save total mean dataframes
    media_tono_mensual.to_csv("./data_final/media_tono_mensual/media_tono_mensual.csv", index=True)
    media_popularity_mensual.to_csv("./data_final/media_popularity_mensual/media_popularity_mensual.csv", index=True)
    media_tono_trimestral.to_csv("./data_final/media_tono_trimestral/media_tono_trimestral.csv", index=True)
    media_popularity_trimestral.to_csv("./data_final/media_popularidad_trimestral/media_popularity_trimestral.csv", index=True)
    return "Mean values calculated and saved successfully."

