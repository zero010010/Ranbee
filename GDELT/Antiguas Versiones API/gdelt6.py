from fastapi import FastAPI
from gdeltdoc import GdeltDoc, Filters
import pandas as pd
import os
import datetime

app = FastAPI()

# 3 ENDPOINTS PARA EXTRAER DATOS DE GDELT, uno para la limpieza, 2 para cambiar a mensual y trimestral 
# (lo que se nos solicita) Y UNO FINAL CON TODOS LOS CSV POR PAISES, MENSUAL TRIMESTRAL Y TOPIC
@app.get("/articles/") 
def get_articles(keyword: str, country: str, descarga: str):
    f = Filters(keyword=keyword,
        start_date="2017-01-01", # TRAS VARIAS REVISIONES, PONEMOS EL MISMO FILTRO DE TIEMPO PARA TODAS LAS BUSQUEDAS, PODRIAMOS CAMBIARLO SI QUEREMOS Y METERLO COMO PARAMETRO EXTRA
        end_date="2024-04-05",
        country=country)
    gd = GdeltDoc()
    articles = gd.article_search(f)
    df = pd.DataFrame(articles)
    if descarga.lower() == "yes": # Para guardar el archivo si el parametro descarga es YES
        if not os.path.exists("./data/articulos"): # Comprobar si la carpeta "/data/articulos" existe, si no, crearla
            os.makedirs("./data/articulos")
        file_number = 1  
        while os.path.exists(f"./data/articulos/csv_articulos_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
            file_number += 1
        filename = f"./data/articulos/csv_articulos_{file_number}.csv"
        df.to_csv(filename, index=False)
    
    return df

@app.get("/tone/") # PARA EL TONO, DIARIO
def get_tone_results(keyword: str, country: str,descarga: str):
    f = Filters(keyword=keyword,
        start_date="2017-01-01", # TRAS VARIAS REVISIONES, PONEMOS EL MISMO FILTRO DE TIEMPO PARA TODAS LAS BUSQUEDAS, PODRIAMOS CAMBIARLO SI QUEREMOS Y METERLO COMO PARAMETRO EXTRA
        end_date="2024-04-05",
        country=country)
    gd = GdeltDoc()
    tone_results = gd.timeline_search("timelinetone", f)
    df_tono = pd.DataFrame(tone_results)
    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
        if not os.path.exists("./data/tono"): # Comprobar si la carpeta "../data/articulos" existe, si no, crearla
            os.makedirs("./data/tono")
        file_number = 1  
        while os.path.exists(f"./data/tono/csv_tono_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
            file_number += 1
        filename = f"./data/tono/csv_tono_{file_number}.csv"
        df_tono.to_csv(filename, index=False)
    
    return df_tono

# Ejemplo prueba print(get_tone_results("Inclusive growth","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"]))

@app.get("/popularity/") # PARA LA POPULARIDAD, DIARIO
# Funcion popularidad, mismo cambio para que no se sobreescriban,, y creacion del bucle con el parametro 
# descarga para elegir si obtener el csv o no
def get_popularity_results(keyword: str, country: str,descarga: str):
    f = Filters( keyword=keyword,
        start_date="2017-01-01", # TRAS VARIAS REVISIONES, PONEMOS EL MISMO FILTRO DE TIEMPO PARA TODAS LAS BUSQUEDAS, PODRIAMOS CAMBIARLO SI QUEREMOS Y METERLO COMO PARAMETRO EXTRA
        end_date="2024-04-05",
        country=country)
    gd = GdeltDoc()
    popularity_results = gd.timeline_search("timelinenvol", f) 
    df_popularidad = pd.DataFrame(popularity_results)
    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
        # Comprobar si la carpeta "./data/popularidad" existe, si no, crearla
        if not os.path.exists("./data/popularidad"):
            os.makedirs("./data/popularidad")
        file_number = 1  
        while os.path.exists(f"./data/popularidad/csv_popularidad_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
            file_number += 1
        filename = f"./data/popularidad/csv_popularidad_{file_number}.csv"
        df_popularidad.to_csv(filename, index=False)
    
    return df_popularidad
# EJEMPLO HECHO print(get_popularity_results("Inclusive growth","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"]))

# PARA LA FUNCION DE LIMPIEZA, FUNCION AUXILIAR
def limpiar_dataframe(df: pd.DataFrame,freq:str): # PARA EL TIPO DE FRECUENCIA QUE QUEREMOS, DIARIO, MENSUAL O TRIMESTRAL
    # Nos aseguramos que el DataFrame tenga todas las fechas. Si alguna no está, rellenamos con 0.
    start_date = df['datetime'].min()
    end_date = df['datetime'].max()
    all_dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    df = df.set_index('datetime').reindex(all_dates).fillna(0).reset_index()
    df = df.rename(columns={'index': 'datetime'}) # Renombramos la columna del índice
    df_limpio= df.dropna().drop_duplicates()
    return df_limpio # creo la funcion primero, que luego podre usar para cualquier DataFrame. 
                    #Metemos solo los nulos y duplicados en un primer momento


# Endpoint para limpiar los datos (este incluiría solo estas tres funciones),no se si podríamos hacerlo en general
@app.get("/limpieza")
def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, country: str): # LOS PARAMETROS NECESARIOS
    if funcion_obtener_datos == "articles":
        df = get_articles(keyword, country, "no") # PODEMOS INCLUIR EL PARAMETRO DE DESCARGA EN LA FUNCION O DIRECTAMENTE PONER NO AQUI
    elif funcion_obtener_datos == "tone":
        df = get_tone_results(keyword, country,"no")
    elif funcion_obtener_datos == "popularity":
        df = get_popularity_results(keyword, country,"no")
    else:
        return {"mensaje": "Función de obtener datos no válida"}
    
    df_limpio = limpiar_dataframe(df,"D") # PONEMOS DIARIO PORQUE LAS FUNCIONES DE LAS QUE DERIVA ESTE ENDPOINT TIENEN RANGO DIARIO

    carpeta_padre = "data_limpio" # Creamos la carpeta padre "data_limpio" si no existe
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}_limpios" # luego la ruta de la segunda carpeta
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # y despues la del archivo csv
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_limpios_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_limpios_{file_number}.csv"
    df_limpio.to_csv(filename, index=False)
    
    return {"mensaje": f"Datos de {funcion_obtener_datos} limpiados y guardados exitosamente en '{filename}'"}

# EJEMPLO HECHO endpoint_limpiar_dataframe("articles","Unemployement Benefits","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"])

@app.get("/limpieza/mensual") # PARA METER LOS PAISES QUE QUIERAS, MAXIMO 9, Y ES DIARIO, porque asi lo hemos decidido!!
def descargar_datos_mensuales(funcion_obtener_datos: str, keyword: str, country: str):
    if funcion_obtener_datos == "tone":
        df = get_tone_results(keyword, country,"no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Agrupamos los datos por mes y calculamos la suma de los valores para cada mes
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
    elif funcion_obtener_datos == "popularity":
        df = get_popularity_results(keyword, country,"no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()

    else:
        return {"mensaje": "Función de obtener datos no válida"}
    
    df_mensual_limpio = limpiar_dataframe(df_monthly,"M") # LLAMAMOS A LA FUNCION LIMPIAR DATAFRAME

    carpeta_padre = "data_mensual_limpio" # Creamos la carpeta padre "data_limpio" si no existe
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}_limpios" # luego la ruta de la segunda carpeta
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # y despues la del archivo csv
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_limpios_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_limpios_mensual_{file_number}.csv"
    df_mensual_limpio.to_csv(filename, index=False)
    
    return {"mensaje": f"Datos de {funcion_obtener_datos} limpiados y guardados exitosamente en '{filename}'"}

@app.get("/limpieza/trimestral") # PARA METER LOS PAISES QUE QUIERAS, MÁXIMO 9
def descargar_datos_trimestrales(funcion_obtener_datos: str, keyword: str, country: str):
    if funcion_obtener_datos == "tone":
        df = get_tone_results(keyword, country,"no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Agrupamos los datos por trimestre y calculamos la suma de los valores para cada trimestre
        df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
    elif funcion_obtener_datos == "popularity":
        df = get_popularity_results(keyword, country,"no")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index()
    else:
        return {"mensaje": "Función de obtener datos no válida"}
    
    df_trimestral_limpio = limpiar_dataframe(df_trimestral,"Q") # LLAMAMOS A LA FUNCION LIMPIAR DATAFRAME

    carpeta_padre = "data_trimestral_limpio" # Creamos la carpeta padre "data_limpio" si no existe
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}_limpios" # luego la ruta de la segunda carpeta
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # y despues la del archivo csv
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_limpios_trimestral_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_{country}_limpios_{file_number}.csv"
    df_trimestral_limpio.to_csv(filename, index=False)
    
    return {"mensaje": f"Datos de {funcion_obtener_datos} limpiados y guardados exitosamente en '{filename}'"}

@app.get("/Proyecto")
def extraccion_total(funcion_obtener_datos: str, keyword: str, time: str):
    countries = ['AU', 'BE', 'SZ', 'CY', 'EZ', 'GM', 'DA', 'GR', 'SP', 'FI', 'FR', 'EI', 'IT', 'LU', 'NL', 'NO', 'PO', 'SW', 'SI']
    
    for country in countries:
        f = Filters(keyword=keyword,
                    start_date="2017-01-01",
                    end_date="2024-04-05",
                    country=country)
        gd = GdeltDoc() 
        
        if funcion_obtener_datos.lower() == "tone":
            results = gd.timeline_search("timelinetone", f)
            df = pd.DataFrame(results)
            folder_name = "tono"
        elif funcion_obtener_datos.lower() == "popularity":
            results = gd.timeline_search("timelinevol", f)
            df = pd.DataFrame(results)
            folder_name = "popularity"
        else:
            return "Error: La función de extracción de datos especificada no es válida."
        
        if time.lower() == "mensual":
            df['datetime'] = pd.to_datetime(df['datetime'])
            df_monthly = df.groupby(pd.Grouper(key='datetime', freq='M')).sum().reset_index()
            save_folder = f"./data_final/{folder_name}/mensual"
            df_save = df_monthly
            df_save = limpiar_dataframe(df_save, "M") # LIMPIEZA MENSUAL
        elif time.lower() == "trimestral":
            df['datetime'] = pd.to_datetime(df['datetime'])
            df_trimestral = df.groupby(pd.Grouper(key='datetime', freq='Q')).sum().reset_index() 
            save_folder = f"./data_final/{folder_name}/trimestral"
            df_save = df_trimestral
            df_save = limpiar_dataframe(df_save,"Q") # LIMPIEZA EN TRIMESTRES
            
        else:
            return "Error: El intervalo especificado no es válido."
        

        os.makedirs(save_folder, exist_ok=True) # para asegurarnos de que la carpeta este

        # y guardamos
        file_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # para evitar sobreescribir
        filename = f"{save_folder}/{keyword}_csv_{folder_name}_{time}_{country}_{file_timestamp}.csv"  # Agregar el nombre del país y el periodo de tiempo al archivo CSV
        df_save.to_csv(filename, index=False)
    
    return f"Mean of {funcion_obtener_datos.capitalize()} data downloaded successfully for all countries"

# ULTIMISIMO CAMBIO, CREAMOS DOS LLAMADAS NUEVAS, UNA PARA DATOS MENSUALES Y OTRA PARA TRIMESTRALES DE TONO Y POPULARIDAD
# creamos una ultima llamada que aune todo, para la extraccion completa por países de tono y popularidad
# PROBLEMAS ENCONTRADOS!! PROBLEMAS CON LA CREACION DE LA CARPETA , SOLUCION  os.makedirs(save_folder, exist_ok=True)
# Problema, para evitar los dias faltantes, meti en la funcion de limpieza una reindexacion, pero DEPENDE DEL PERIODO
# QUE PONGAS TE RELLENA TODOS LOS HUECOS (D,M O Q)
# SOLUCION, meti un parametro en la funcion de limpieza, para elegir D (DIARIO),M(MENSUAL) O Q(TRIMESTRE). 
# DENTRO DE LA FUNCION PROYECTO, YA ESTA INCLUIDO SI ES MENSUAL O POR TRIMESTRES.