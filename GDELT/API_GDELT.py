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

def funcion_obtener_datos(funcion_obtener_datos: str, keyword: str, country: str, descarga: str):
    """
    Retrieves daily data from the GDELT API and filters by the specified keyword and country. 
    If "descarga" is set to "yes", 
    saves the data to a CSV file.

    Args:
        funcion_obtener_datos (str): Type of data , either "tone" or "popularity".
        keyword (str): keyword to search for.
        country (str): country to filter .
        descarga (str): download to a CSV file ("yes") or not ("no").

    Returns:
        pandas.DataFrame: data TO Pandas DataFrame.
    """
def descargar_datos_diarios(funcion_obtener_datos: str, keyword: str, country: str,descarga: str):   
    f = Filters(keyword=keyword, 
                    start_date="2017-01-01",
                    end_date="2023-12-31",
                    country=country)
    gd = GdeltDoc() # Initialize GdeltDoc class 
    if funcion_obtener_datos.lower() == "tone":# Checks if tone is specified
        results = gd.timeline_search("timelinetone", f)# Calls timeline_search method based on filter
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
        if not os.path.exists(carpeta_tipo_datos):# Check if subfolder exists
            os.makedirs(carpeta_tipo_datos)# If not, create it
    
        # Check if file with same name already exists, if so, increment file number 
        file_number = 1
        while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):# Check if file with same name already exists
            file_number += 1# Check if file with same name already exists, if so, increment file
        filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_diarios_{file_number}.csv"# Create filename with incremented number
        df.to_csv(filename, index=False)# Save DataFrame to CSV file
    
    return df

"""
def descargar_datos_mensuales: Defines a GET endpoint for downloading monthly data for countries.

download monthly data for a specified keyword and country. 
It first calls
  `descargar_datos_diarios` function to retrieve the daily data, 
 then groups the data by month and sums the values. 
 The resulting monthly data is then saved to a CSV file in the "data_mensual" directory,
   with a subfolder for the specific data type (tone or popularity).

Args:
    funcion_obtener_datos (str): The type of data to download, either "tone" or "popularity".
    keyword (str): The keyword to search for.
    country (str): The country to filter the data by.

Returns:
    str: A message indicating that the data was downloaded successfully.
"""

@app.get("/monthly/extraction") # Defines a GET endpoint for downloading monthly data for countries
def descargar_datos_mensuales(funcion_obtener_datos: str, keyword: str, country: str):# Function to download monthly data, arg : data type, keyword,
    if funcion_obtener_datos == "tone":# Checks if tone is specified
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no") # function avoids downloading again
        df['datetime'] = pd.to_datetime(df['datetime'])# convert datetime column to datetime
        
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()# group by month and sum values
    elif funcion_obtener_datos == "popularity":# Checks if popularity is specified
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country,"no")# function avoids downloading again
        df['datetime'] = pd.to_datetime(df['datetime'])# convert datetime column to datetime
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index() # group by month and sum values

    else:
        return {"mensaje": "Función de obtener datos no válida"}

    carpeta_padre = "data_mensual" # creat parent folder
    if not os.path.exists(carpeta_padre): # Check if parent folder exists, if not create it
        os.makedirs(carpeta_padre)# If not, create it
    
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
@app.get("/quaterly/extraction")

    """
    Defines a GET endpoint for downloading quarterly data for countries.

    download quarterly data for a specified keyword and country. It first calls
    the `descargar_datos_diarios` function to retrieve the daily data,
      then groups the data by quarter and sums the values.
    The resulting quarterly data is then saved to a CSV file in the "data_trimestral" directory,
    with a subfolder for the specific data type (tone or popularity).

    Args:
        funcion_obtener_datos (str): type of data to download, either "tone" or "popularity".
        keyword (str): keyword to search for.
        country (str): country to filter the data by.

    Returns:
        str: A message indicating that the data was downloaded successfully.
    """
    

def descargar_datos_trimestrales(funcion_obtener_datos: str, keyword: str, country: str):# Function to download quarterly data, arg : data type, keyword, country
    if funcion_obtener_datos == "tone":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        # groupby quarter and sum values
        df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
    elif funcion_obtener_datos == "popularity":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")# Call daily data function
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() # groupby quarter and sum values
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


"""
Cleans a DataFrame by converting the datetime column to datetime type, filling missing dates with 0, 
and removing any rows with NaN values or duplicate rows.

Args:
    df (pd.DataFrame): The DataFrame to be cleaned.
    freq (str): The frequency to use when creating the date range.

Returns:
    pd.DataFrame: The cleaned DataFrame.
"""
def limpiar_dataframe(df: pd.DataFrame,freq:str): # function to clean dataframe, arg : dataframe, frequency
    # Convert datetime column to datetime type, it fills missing dates with 0
    start_date = df['datetime'].min()# Get min date
    end_date = df['datetime'].max()# Get max date
    all_dates = pd.date_range(start=start_date, end=end_date, freq=freq)# Create date range between start and end date
    df = df.set_index('datetime').reindex(all_dates).fillna(0).reset_index()# fill missing dates with 0
    df = df.rename(columns={'index': 'datetime'}) # rename datetime column as datetime
    df_limpio= df.dropna().drop_duplicates()# drop na and duplicate values
    return df_limpio 


# Cleanup function, pending revision and include more utilities, such as mean and Dataframe concatenation
@app.get("/clean")

def limpiar_y_guardar_datos(funcion_obtener_datos: str, keyword: str, country: str, periodo: str):
    """
    Cleans and saves a DataFrame based , keyword, country, and time period.

    Args:
        funcion_obtener_datos (str): type of data to be cleaned (e.g. "tone", "popularity").
        keyword (str): keyword to be used.
        country (str): country to be used.
        periodo (str): The time period to be used (e.g. "monthly", "diary", "quaterly").

    Returns:
        str: A message indicating that the data has been cleaned successfully.
    """
    if funcion_obtener_datos == "tone":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        if periodo == "quaterly":
            df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
        elif periodo == "monthly":
            df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
        elif periodo == "diary":
            df_quaterly = df
        else:
            return {"mensaje": "Período no válido"}
    elif funcion_obtener_datos == "popularity":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        if periodo == "quaterly":
            df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
        elif periodo == "monthly":
            df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
        elif periodo == "diary":
            df_quaterly = df
        else:
            return {"mensaje": "Período no válido"}
    else:
        return {"mensaje": "Función de obtener datos no válida"}

    df_limpio = limpiar_dataframe(df_quaterly, periodo)

    carpeta_padre = "data_limpia"
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)

    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}"
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)

    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{periodo}_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{periodo}_{file_number}.csv"
    df_limpio.to_csv(filename, index=False)

    return f"Data of {funcion_obtener_datos.capitalize()} cleaned and saved successfully"

def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, country: str,periodo:str): # function to clean dataframe, arg : data type, keyword, country, period
    if funcion_obtener_datos.lower() == "tone":
        results = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df = pd.DataFrame(results)# Convert results to DataFrame
        folder_name = "tone"# Set folder name
    elif funcion_obtener_datos.lower() == "popularity":
        results = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df = pd.DataFrame(results)# Convert results to DataFrame
        folder_name = "popularity" # Set folder name
    else:
        return "Error: La función de extracción de datos especificada no es válida."
        
    if periodo.lower() == "monthly":
        df['datetime'] = pd.to_datetime(df['datetime'])# convert datetime column to datetime
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()# group by month and sum values
        save_folder = f"./data_limpio/{folder_name}/monthly"# Set save folder
        df_save = df_monthly# Assign monthly dataframe to clean
        df_save = limpiar_dataframe(df_save, "M") # Monthly data cleaning
    elif periodo.lower() == "diary":
        save_folder = f"./data_limpio/{folder_name}/diary"# Set save folder
        df_save = limpiar_dataframe(df,"D")
    elif periodo.lower() == "quaterly":
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() # group by quarter and sum values
        save_folder = f"./data_limpio/{folder_name}/quaterly"# Set save folder
        df_save = df_trimestral# Assign quarterly dataframe to clean
        df_save = limpiar_dataframe(df_save,"Q") # clean quarterly data
            
    else:
        return "Error: El intervalo especificado no es válido."
        
    os.makedirs(save_folder, exist_ok=True) # create folder if not exists

    # save cleaned dataframe to csv file
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # avoid re-writing existing files by adding timestamp to filename
    filename = f"{save_folder}/{keyword}_limpio_{folder_name}_{periodo}_{country}_{file_timestamp}.csv"  # Agregar el nombre del país y el periodo de tiempo al archivo CSV
    df_save.to_csv(filename, index=False)# Save cleaned DataFrame to CSV file with timestamp in filename to avoid overwriting
    
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
                    start_date="2017-01-01",# define start/end date range
                    end_date="2023-12-31",
                    country=country)# add country to filter
        gd = GdeltDoc() 
        
        if funcion_obtener_datos.lower() == "tone":
            results = gd.timeline_search("timelinetone", f)# call timeline_search passing filter
            df = pd.DataFrame(results)# convert results to dataframe
            folder_name = "tone"# set folder name
        elif funcion_obtener_datos.lower() == "popularity":# check data type
            results = gd.timeline_search("timelinevol", f)# call timeline_search passing filter
            df = pd.DataFrame(results)# convert results to dataframe
            folder_name = "popularity"
        else:
            return "Error: La función de extracción de datos especificada no es válida."
        
        if periodo.lower() == "monthly":# check period
            df['datetime'] = pd.to_datetime(df['datetime'])# convert datetime column to datetime
            df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()# group by month and sum values, reset index for saving
            save_folder = f"./data_final/{folder_name}/monthly/{keyword}" # Set save folder
            df_save = df_monthly# Assign monthly dataframe to clean
            df_save = limpiar_dataframe(df_save, "M") # monthly data cleaning
        elif periodo.lower() == "quaterly":# check period == "quaterly"
            df['datetime'] = pd.to_datetime(df['datetime'])# convert datetime column to datetime
            df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() # group by quarter and sum values, reset index for saving
            save_folder = f"./data_final/{folder_name}/quaterly/{keyword}"# Set save folder with quaterly folder
            df_save = df_trimestral #Assign quarterly dataframe to clean
            df_save = limpiar_dataframe(df_save,"Q") # quartely data for cleaning   
            
        else:
            return "Error: El intervalo especificado no es válido."
        
        os.makedirs(save_folder, exist_ok=True) # create folder if not exists
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # avoid re-writing existing files by adding timestamp to filename
        filename = f"{save_folder}/{keyword}_{folder_name}_{periodo}_{country}_{file_timestamp}.csv"  # Agregate country name and time period to csv filename
        df_save.to_csv(filename, index=False)# save cleaned dataframe to csv file with timestamp in filename
    
    return f"Mean of {funcion_obtener_datos.capitalize()} data downloaded successfully for all countries"

@app.get("/eda/") # perform basic exploratory data analysis
@app.get("/eda/")
def eda(data_source: str, keyword: str, country: str, frequency: str):
    """
    Performs exploratory data analysis (EDA) on the downloaded data from the GDELT API.

    Args:
        data_source (str): data source to analyze
        keyword (str): keyword used to download the data.
        country (str): country 
        frequency (str): frequency of the data, either "monthly" or "quaterly".

    Returns:
        dict: A dictionary containing the results of the EDA, 
        including the number of rows and columns, 
        column names, null value counts, data types, 
        and descriptive statistics.
    """
    
   

def perform_eda(data_source: str, keyword: str, country: str, frequency: str): # function to perform eda, arg : data source, keyword, country, frequency
    if data_source == "tone": # check data source
        if frequency.lower() == "diary":# check frequency
            df = descargar_datos_diarios("tone", keyword, country, "no")# call diary data download function
        elif frequency.lower() == "monthly":
            df = descargar_datos_mensuales("tone", keyword, country)# call monthly data download function
        elif frequency.lower() == "quaterly":
            df = descargar_datos_trimestrales("tone", keyword, country)# 
        else:
            return {"error": "Invalid frequency"}

    elif data_source == "popularity":# check data source
        if frequency.lower() == "diary":
            df = descargar_datos_diarios("popularity", keyword, country, "no")# call diary data download function
        elif frequency.lower() == "monthly":
            df = descargar_datos_mensuales("popularity", keyword, country)# call monthly data download function
        elif frequency.lower() == "quaterly":
            df = descargar_datos_trimestrales("popularity", keyword, country)# call quarterly data download function
        else:
            return {"error": "Invalid frequency"}

    else:
        return {"error": "Invalid data source"}

    eda_results = {
        "num_rows": len(df),  # number of rows
        "num_columns": len(df.columns),  # number of columns
        "column_names": list(df.columns),  # List of column names
        "null_counts": df.isnull().sum().to_dict(),  # Count of null values por columna
        "data_types": df.dtypes.to_dict(),  # Types of data por columna
        "descriptive_stats": df.describe().to_dict()} # Descriptive stats 

    eda_folder = "EDA"# create EDA folder
    if not os.path.exists(eda_folder):# check if folder exists
        os.makedirs(eda_folder)# create folder

    
    file_number = 1
    while os.path.exists(f"{eda_folder}/eda_{data_source}_{file_number}.csv"):# loop through csv files in folder
        file_number += 1    # increment file number
    filename = f"{eda_folder}/eda_{data_source}_{file_number}.csv"# generate new filename
    eda_df = pd.DataFrame.from_dict(eda_results, orient="index")# convert results dict to dataframe
    eda_df.to_csv(filename, index=False)# save dataframe to csv with generated filename

    return {"message": f"EDA results for {data_source} saved to {filename}"}

# OPTIONAL, PENDING REVIEW, not ready
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
@app.get("/total_mean/")
def total_mean(monthly_folder, quarterly_folder):
    """
    Calculates the mean values of the 'Average Tone' and 'Volume Intensity' columns across all CSV files
      in the specified monthly and quarterly folders, 
      saves the results to CSV files.

    Returns:
        str: message: "Mean values calculated and saved successfully."

    """
def total_mean():
# folder routes
    tono_mensual_csv_folder = "./data_final/tone/monthly"# folder for tone monthly csvs
    popularity_mensual_csv_folder = "./data_final/popularity/monthly"# folder for popularity monthly csvs
    tono_trimestral_csv_folder = "./data_final/tone/quaterly"# folder for tone quaterly csvs
    popularity_trimestral_csv_folder = "./data_final/popularity/quaterly"# folder for popularity quaterly csvs

    # mean tone / popularity monthly and quaterly   
    media_tono_mensual = calcular_media(tono_mensual_csv_folder, 'Average Tone')# calculate mean tone monthly
    media_popularity_mensual = calcular_media(popularity_mensual_csv_folder, 'Volume Intensity')# calculate mean popularity monthly
    media_tono_trimestral = calcular_media(tono_trimestral_csv_folder, 'Average Tone')# calculate mean tone quaterly
    media_popularity_trimestral = calcular_media(popularity_trimestral_csv_folder, 'Volume Intensity')# calculate mean popularity quaterly

    # Save total mean dataframes
    media_tono_mensual.to_csv("./data_final/media_tono_mensual/media_tono_mensual.csv", index=True)# Save tone monthly as csv , index =True to save index
    media_popularity_mensual.to_csv("./data_final/media_popularity_mensual/media_popularity_mensual.csv", index=True)# Save popularity monthly as csv , index =True to save index
    media_tono_trimestral.to_csv("./data_final/media_tono_trimestral/media_tono_trimestral.csv", index=True)# Save tone quaterly as csv , index =True to save index
    media_popularity_trimestral.to_csv("./data_final/media_popularidad_trimestral/media_popularity_trimestral.csv", index=True)# Save popularity quaterly as csv , index =True to save index
    return "Mean values calculated and saved successfully."

