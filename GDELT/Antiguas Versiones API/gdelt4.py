from fastapi import FastAPI
from gdeltdoc import GdeltDoc, Filters
import pandas as pd
import os

app = FastAPI()

# 3 ENDPOINTS PARA EXTRAER DATOS DE GDELT y uno para la limpieza 
@app.get("/articles/") 
def get_articles(keyword: str, country: str, descarga: str):
    f = Filters(keyword=keyword,
        start_date="2017-01-01", # TRAS VARIAS REVISIONES, PONEMOS EL MISMO FILTRO DE TIEMPO PARA TODAS LAS BUSQUEDAS, PODRIAMOS CAMBIARLO SI QUEREMOS Y METERLO COMO PARAMETRO EXTRA
        end_date="2024-04-05",
        country=country)
    gd = GdeltDoc()
    articles = gd.article_search(f)
    df = pd.DataFrame(articles)
    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
        if not os.path.exists("./data/articulos"): # Comprobar si la carpeta "/data/articulos" existe, si no, crearla
            os.makedirs("./data/articulos")
        file_number = 1  
        while os.path.exists(f"./data/articulos/csv_articulos_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
            file_number += 1
        filename = f"./data/articulos/csv_articulos_{file_number}.csv"
        df.to_csv(filename, index=False)
    
    return df

@app.get("/tone/") # PARA EL TONO, hemos modificado 
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

@app.get("/popularity/") # PARA LA POPULARIDAD
# Funcion popularidad, mismo cambio para que no se sobreescriban,, y creacion del bucle con el parametro 
# descarga para elegir si obtener el csv o no
def get_popularity_results(keyword: str, country: str,descarga: str):
    f = Filters( keyword=keyword,
        start_date="2017-01-01", # TRAS VARIAS REVISIONES, PONEMOS EL MISMO FILTRO DE TIEMPO PARA TODAS LAS BUSQUEDAS, PODRIAMOS CAMBIARLO SI QUEREMOS Y METERLO COMO PARAMETRO EXTRA
        end_date="2024-04-05",
        country=country)
    gd = GdeltDoc()
    popularity_results = gd.timeline_search("timelinesourcecountry", f) # CAMBIAMOS timelinevoL POR timelinesourcecountry PARA QUE DIVIDAN POR PAISES
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
def limpiar_dataframe(df: pd.DataFrame):
    df_limpio= df.dropna().drop_duplicates()
    return df_limpio # creo la funcion primero, que luego podre usar para cualquier DataFrame. 
                    #Metemos solo los nulos y duplicados en un primer momento


# Endpoint para limpiar los datos (este incluiría solo estas tres funciones),no se si podríamos hacerlo en general
@app.get("/limpieza/")
def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, country: str): # LOS PARAMETROS NECESARIOS
    if funcion_obtener_datos == "articles":
        df = get_articles(keyword, country, "no") # PODEMOS INCLUIR EL PARAMETRO DE DESCARGA EN LA FUNCION O DIRECTAMENTE PONER NO AQUI
    elif funcion_obtener_datos == "tone":
        df = get_tone_results(keyword, country,"no")
    elif funcion_obtener_datos == "popularity":
        df = get_popularity_results(keyword, country,"no")
    else:
        return {"mensaje": "Función de obtener datos no válida"}
    
    df_limpio = limpiar_dataframe(df) # LLAMAMOS A LA FUNCION LIMPIAR DATAFRAME

    carpeta_padre = "data_limpio" # Creamos la carpeta padre "data_limpio" si no existe
    if not os.path.exists(carpeta_padre):
        os.makedirs(carpeta_padre)
    
    carpeta_tipo_datos = f"{carpeta_padre}/{funcion_obtener_datos}_limpios" # luego la ruta de la segunda carpeta
    if not os.path.exists(carpeta_tipo_datos):
        os.makedirs(carpeta_tipo_datos)
    
    # y despues la del archivo csv
    file_number = 1
    while os.path.exists(f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_limpios_{file_number}.csv"):
        file_number += 1
    filename = f"{carpeta_tipo_datos}/csv_{funcion_obtener_datos}_limpios_{file_number}.csv"
    df_limpio.to_csv(filename, index=False)
    
    return {"mensaje": f"Datos de {funcion_obtener_datos} limpiados y guardados exitosamente en '{filename}'"}

# EJEMPLO HECHO endpoint_limpiar_dataframe("articles","Unemployement Benefits","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"])

# Ultimo cambio,inclusion en carpetas individuales de los 4 endpoints(incluido el de limpieza, que daba error anteriormente)
# HE DEJADO A MEDIAS LA FUNCION DE LIMPIAR DATAFRAME CON LOS MESES Y LOS TRIMESTRES, POR EL PROBLEMA DE LA DIFERENCIA
# ENTRE ARTICLES Y EL TONO Y LA POPULARIDAD (tendremos que pasar a mensuales solo esos 2, no articles, que no esta 
# a volumen mensual, SINO CUANDO SE HAN CREADO LOS ARTICULOS)
# PENSAR SI HACERLO EN EL ENDPOINT DE LIMPIEZA DIRECTAMENTE, EN LA PARTE TONE Y POPULARITY
    # Pondremos dos opciones, a mensual y a trimestral
    #df_limpio['datetime'] = pd.to_datetime(df['fecha'])
    # Pasar a mensual
    #data_monthly = df_limpio.groupby(pd.Grouper(freq='M')).mean() 
    # Agrupar los datos por trimestre y calcular la suma de los valores para cada trimestre
    #df_trimestral = df_limpio.groupby(pd.Grouper(key='fecha', freq='Q')).sum().reset_index()

