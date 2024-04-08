from fastapi import FastAPI
from gdeltdoc import GdeltDoc, Filters
import pandas as pd
import os
import datetime
import time

app = FastAPI()

# 3 ENDPOINTS PARA EXTRAER DATOS DE GDELT, diario, mensual y trimestralmente, uno para la limpieza, 
# (lo que se nos solicita) Y UNO FINAL para nuestro proyecto en particular, con el filtro de nuestros países útiles
# CON TODOS LOS CSV POR PAISES, MENSUAL TRIMESTRAL Y TOPIC
@app.get("/diary/extraction") # PARA METER LOS PAISES QUE QUIERAS, MAXIMO 9
def descargar_datos_diarios(funcion_obtener_datos: str, keyword: str, country: str,descarga: str):   
    f = Filters(keyword=keyword,
                    start_date="2017-01-01",
                    end_date="2023-12-31",
                    country=country)
    gd = GdeltDoc() 
    if funcion_obtener_datos.lower() == "tone":
        results = gd.timeline_search("timelinetone", f)
        df = pd.DataFrame(results)
    elif funcion_obtener_datos.lower() == "popularity":
        results = gd.timeline_search("timelinevol", f)
        df = pd.DataFrame(results)

    else:
        return "Error: La función de extracción de datos especificada no es válida."

    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
        carpeta_padre = "data_diario" # Creamos la carpeta padre "data_diario" si no existe
        if not os.path.exists(carpeta_padre):
            os.makedirs(carpeta_padre)
    
        carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}" # luego la ruta de la segunda carpeta
        if not os.path.exists(carpeta_tipo_datos):
            os.makedirs(carpeta_tipo_datos)
    
        # y despues la del archivo csv
        file_number = 1
        while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):
            file_number += 1
        filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_diarios_{file_number}.csv"
        df.to_csv(filename, index=False)
    
    return df


@app.get("/monthly/extraction") # PARA METER LOS PAISES QUE QUIERAS, MAXIMO 9
def descargar_datos_mensuales(funcion_obtener_datos: str, keyword: str, country: str):
    if funcion_obtener_datos == "tone":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no") # para que no se descarguen diarios
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Agrupamos los datos por mes y calculamos la suma de los valores para cada mes
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
    elif funcion_obtener_datos == "popularity":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country,"no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()

    else:
        return {"mensaje": "Función de obtener datos no válida"}

    carpeta_padre = "data_mensual" # Creamos la carpeta padre "data_limpio" si no existe
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}" # luego la ruta de la segunda carpeta
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # y despues la del archivo csv
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_mensual_{file_number}.csv"
    df_monthly.to_csv(filename, index=False)
    
    return f"Data of {funcion_obtener_datos.capitalize()} downloaded successfully"

@app.get("/quaterly/extraction") # PARA METER LOS PAISES QUE QUIERAS, MÁXIMO 9
def descargar_datos_trimestrales(funcion_obtener_datos: str, keyword: str, country: str):
    if funcion_obtener_datos == "tone":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Agrupamos los datos por trimestre y calculamos la suma de los valores para cada trimestre
        df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
    elif funcion_obtener_datos == "popularity":
        df = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_quaterly = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
    else:
        return {"mensaje": "Función de obtener datos no válida"}

    carpeta_padre = "data_trimestral" # Creamos la carpeta padre "data_limpio" si no existe
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}" # luego la ruta de la segunda carpeta
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # y despues la del archivo csv
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_{file_number}.csv"
    df_quaterly.to_csv(filename, index=False)
    
    return f"Data of {funcion_obtener_datos.capitalize()} downloaded successfully"

# PARA LA FUNCION DE LIMPIEZA, FUNCION AUXILIAR
def limpiar_dataframe(df: pd.DataFrame,freq:str): # PARA EL TIPO DE FRECUENCIA QUE QUEREMOS, DIARIO, MENSUAL O TRIMESTRAL
    # Nos aseguramos que el DataFrame tenga todas las fechas. Si alguna no está, rellenamos con 0.
    start_date = df['datetime'].min()
    end_date = df['datetime'].max()
    all_dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    df = df.set_index('datetime').reindex(all_dates).fillna(0).reset_index()
    df = df.rename(columns={'index': 'datetime'}) # Renombramos la columna del índice
    df_limpio= df.dropna().drop_duplicates()
    return df_limpio 


# Endpoint para limpiar los datos
@app.get("/clean")
def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, country: str,periodo:str): # LOS PARAMETROS NECESARIOS
    if funcion_obtener_datos.lower() == "tone":
        results = descargar_datos_diarios(funcion_obtener_datos, keyword, country, "no")
        df = pd.DataFrame(results)
        folder_name = "tone"
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
        df_save = limpiar_dataframe(df_save, "M") # LIMPIEZA MENSUAL
    elif periodo.lower() == "diary":
        save_folder = f"./data_limpio/{folder_name}/diary"
        df_save = limpiar_dataframe(df,"D")
    elif periodo.lower() == "quaterly":
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() 
        save_folder = f"./data_limpio/{folder_name}/quaterly"
        df_save = df_trimestral
        df_save = limpiar_dataframe(df_save,"Q") # LIMPIEZA EN TRIMESTRES
            
    else:
        return "Error: El intervalo especificado no es válido."
        
    os.makedirs(save_folder, exist_ok=True) # para asegurarnos de que la carpeta este

    # y guardamos
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # para evitar sobreescribir
    filename = f"{save_folder}/{keyword}_limpio_{folder_name}_{time}_{country}_{file_timestamp}.csv"  # Agregar el nombre del país y el periodo de tiempo al archivo CSV
    df_save.to_csv(filename, index=False)
    
    return f"Dates of {funcion_obtener_datos.capitalize()} has been cleaned successfully"

# EJEMPLO HECHO endpoint_limpiar_dataframe("articles","Unemployement Benefits","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"])

@app.get("/project") # con bucle para descargar todos los csv de los paises
def extraccion_total(funcion_obtener_datos: str, keyword: str, periodo: str):
    countries = ['Austria', 'Belgium', 'Switzerland', 'Cyprus', 'EZ', 'Germany', 'Denmark', 'Greece', 'Spain', 'Finland', 'France', 'Ireland', 'Italy', 'Luxembourg', 'Netherlands', 'Norway', 'Portugal', 'Sweden', 'Slovenia']
    for country in countries:
        f = Filters(keyword=keyword,
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
            df_save = limpiar_dataframe(df_save, "M") # LIMPIEZA MENSUAL
        elif periodo.lower() == "quaterly":
            df['datetime'] = pd.to_datetime(df['datetime'])
            df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() 
            save_folder = f"./data_final/{folder_name}/quaterly/{keyword}"
            df_save = df_trimestral
            df_save = limpiar_dataframe(df_save,"Q") # LIMPIEZA EN TRIMESTRES
            
        else:
            return "Error: El intervalo especificado no es válido."
        
        os.makedirs(save_folder, exist_ok=True) # para asegurarnos de que la carpeta este

        # y guardamos
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # para evitar sobreescribir
        filename = f"{save_folder}/{keyword}_{folder_name}_{time}_{country}_{file_timestamp}.csv"  # Agregar el nombre del país y el periodo de tiempo al archivo CSV
        df_save.to_csv(filename, index=False)
    
    return f"Mean of {funcion_obtener_datos.capitalize()} data downloaded successfully for all countries"

@app.get("/mean")
def calcular_media(csv_folder, column_name,output_csv: bool = False): # Por defecto no se descargará
    dfs = []
    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_folder, filename)
            df = pd.read_csv(file_path, parse_dates=['datetime'])
            print(f"Leyendo archivo: {file_path}")
            if column_name in df.columns:
                df.set_index('datetime', inplace=True)
                dfs.append(df[column_name].rename(filename.split('.')[0]))  # Renombrar la serie con el nombre del archivo
            else:
                print(f"La columna '{column_name}' no se encontró en el archivo: {file_path}")

    if not dfs:
        print(f"No se encontraron archivos CSV en el directorio: {csv_folder}")
        return pd.DataFrame()

    combined_df = pd.concat(dfs, axis=1)
    media_columna = combined_df.mean(axis=1)  # Calcular la media a lo largo de las columnas
    media_df = pd.DataFrame({column_name: media_columna})
    if output_csv:
        parent_directory = os.path.dirname(csv_folder)
        output_path = os.path.join(parent_directory, f"media_{column_name}.csv")
        media_df.to_csv(output_path, index=False)
        return {"message": f"Archivo CSV guardado en: {output_path}"}
    else:
        return media_df

@app.get("/total_mean/") # PARA LAS 4 MEDIAS, LLAMADA SOLO PARA ESTE PROYECTO, para obtener los 4 datos al mismo tiempo
def total_mean():
# Rutas de cada carpeta
    tono_mensual_csv_folder = "./data_final/tone/monthly"
    popularity_mensual_csv_folder = "./data_final/popularity/monthly"
    tono_trimestral_csv_folder = "./data_final/tone/quaterly"
    popularity_trimestral_csv_folder = "./data_final/popularity/quaterly"

    # Media por tono y popularidad, mensual y trimestral, usando funcion anterior
    media_tono_mensual = calcular_media(tono_mensual_csv_folder, 'Average Tone')
    media_popularity_mensual = calcular_media(popularity_mensual_csv_folder, 'Volume Intensity')
    media_tono_trimestral = calcular_media(tono_trimestral_csv_folder, 'Average Tone')
    media_popularity_trimestral = calcular_media(popularity_trimestral_csv_folder, 'Volume Intensity')

    # Guardando csv
    media_tono_mensual.to_csv("./data_final/media_tono_mensual/media_tono_mensual.csv", index=True)
    media_popularity_mensual.to_csv("./data_final/media_popularity_mensual/media_popularity_mensual.csv", index=True)
    media_tono_trimestral.to_csv("./data_final/media_tono_trimestral/media_tono_trimestral.csv", index=True)
    media_popularity_trimestral.to_csv("./data_final/media_popularidad_trimestral/media_popularity_trimestral.csv", index=True)
    return "Mean values calculated and saved successfully."

# UN CAMBIO MAS, VOY A AGRUPAR EN DESCARGA DIARIA, MENSUAL Y TRIMESTRAL, EL ENDPOINT DE LIMPIEZA Y EL DEL PROYECTO
# Queremos crear al final uno que aune todos los csv por paises y trimestres y meses.
# creamos la llamada calcular_media_columna_total.
# Problemas encontrados, SALTOS DE CARPETA, no se localizan... SOLUCION, debuggear el código hasta visualizar el error
# Problemas encontrados PUBLIC EXPENDITURE POLICY NO APARECE COMO TOPIC,Jobs tampoco, MSME Finance tampoco, comentar con randbee 
# o buscar mas topics en la documentacion, como UNEMPLOYED O UNEMPLOYMENT ambos válidos..., aqui hay muchos mas http://data.gdeltproject.org/api/v2/guides/LOOKUP-GKGTHEMES.TXT
# PROBLEMA, HAY TOPICS QUE NO LOS HAY EN DETERMINADOS PAISES (EL BUCLE SE HA PARADO EN BELGICA EN HEALTH SERVICE DELIVERY), SOLUCION, TRY EXCEPT Y CONTINUE
# PROBLEMA, como hagas una llamada multiple, hay que esperar 5 segundos entre consultas o deja de funcionar
#Se produjo un error: The gdelt api returned a non-successful statuscode. This is the response message: Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries.
# solucion, meter un timesleep. NO LO HA SOLUCIONADO.
# En principio descarto el doble bucle para los paises y topic.
#keywords = ["Inclusive growth", "Enterprise Development", "Financial Inclusion", "Social inclusion", "Access to Education", "Health service delivery"]
#