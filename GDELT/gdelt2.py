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
    # Comprobar si la carpeta "/data/articulos" existe, si no, crearla
    if not os.path.exists("./data/articulos"):
        os.makedirs("./data/articulos")
    
    file_number = 1  
    while os.path.exists(f"./data/articulos/csv_articulos_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
        file_number += 1
    filename = f"./data/articulos/csv_articulos_{file_number}.csv"
    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
        df.to_csv(filename, index=False)
    
    return df

# Creamos un nuevo parametro, descarga, Y SI ES SI SE DESCARGA Y SI NO, COMO PARA LOS ENDPOINTS DE LIMPIEZA NO SE DESCARGA
# EJEMPLO PRUEBA REALIZADA print(get_articles("Inclusive growth","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"]))

# Otra prueba, esta vez con LA FUNCION tono, A LA QUE HAY QUE AÑADIRLE LO MISMO DE LOS ARTICULOS PARA EVITAR SOBREESCRIBIR
# añadimos el cambio de Fer, con el parametro para descargar o no
# Y SACAMOS LA FECHA DE LOS PARAMETROS DE ENTRADA DE LA LLAMADA
@app.get("/tone/") # PARA EL TONO, hemos modificado 
def get_tone_results(keyword: str, country: str,descarga: str):
    f = Filters(keyword=keyword,
        start_date="2017-01-01", # TRAS VARIAS REVISIONES, PONEMOS EL MISMO FILTRO DE TIEMPO PARA TODAS LAS BUSQUEDAS, PODRIAMOS CAMBIARLO SI QUEREMOS Y METERLO COMO PARAMETRO EXTRA
        end_date="2024-04-05",
        country=country)
    gd = GdeltDoc()
    tone_results = gd.timeline_search("timelinetone", f)
    df_tono = pd.DataFrame(tone_results)
        # Comprobar si la carpeta "../data/articulos" existe, si no, crearla
    if not os.path.exists("./data/tono"):
        os.makedirs("./data/tono")
    file_number = 1  
    while os.path.exists(f"./data/tono/csv_tono_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
        file_number += 1
    filename = f"./data/tono/csv_tono_{file_number}.csv"
    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
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
    # Comprobar si la carpeta "./data/popularidad" existe, si no, crearla
    if not os.path.exists("./data/popularidad"):
        os.makedirs("./data/popularidad")
    file_number = 1  
    while os.path.exists(f"./data/popularidad/csv_popularidad_{file_number}.csv"): # HACEMOS LO MISMO CON EL ARCHIVO, para evitar sobreescribir archivos
        file_number += 1
    filename = f"./data/popularidad/csv_popularidad_{file_number}.csv"
    if descarga.lower() == "yes": # para guardar el archivo si el parametro descarga es YES
        df_popularidad.to_csv(filename, index=False)
    
    return df_popularidad
# EJEMPLO HECHO print(get_popularity_results("Inclusive growth","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"]))

# PARA LA FUNCION DE LIMPIEZA, FUNCION AUXILIAR
def limpiar_dataframe(df: pd.DataFrame):
    df_limpio= df.dropna().drop_duplicates()
    return df_limpio # creo la funcion primero, que luego podre usar para cualquier DataFrame. 
                    #Metemos solo los nulos y duplicados en un primer momento

# EJEMPLO HECHO df = pd.read_csv("csv_articulos_1.csv") PORQUE YA SE HABIA GENERADO, PROBÉ UN DF CUALQUIERA
# OJO, LA FUNCION FUNCIONA, PERO QUITANDO LOS NULOS Y DUPLICADOS HEMOS PERDIDO MUCHISIMOS REGISTROS.
# LA COLUMNA URL_MOBILE TIENE SOLO 21 REGISTROS Y ESO YA NOS QUITA MUCHISIMOS.
# REVISAR ESTO y si tenemos que eliminar columnas con mas de una cantidad de nulos en lugar de las filas,
# poner un threshold de la cantidad de nulos que nos hará eliminar una columna, con que sustituir los nulos en caso 
# de que se mantenga...

# Endpoint para limpiar los datos (este incluiría solo estas tres funciones),no se si podríamos hacerlo en general
@app.get("/limpieza/")
def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, country: str): # LOS PARAMETROS NECESARIOS
    if funcion_obtener_datos == "articles":
        df = get_articles(keyword, country, "no") # PODEMOS INCLUIR EL PARAMETRO DE DESCARGA EN LA FUNCION O DIRECTAMENTE PONER NO AQUI
    elif funcion_obtener_datos == "tone":
        df = get_tone_results(keyword, country, "no")
    elif funcion_obtener_datos == "popularity":
        df = get_popularity_results(keyword, country,"no")
    else:
        return {"mensaje": "Función de obtener datos no válida"}
    
    df_limpio = limpiar_dataframe(df) # LLAMAMOS A LA FUNCION LIMPIAR DATAFRAME
    file_number = 1 # USAMOS EL MISMO BUCLE QUE LOS ENPOINTS PARA EVITAR SOBREESCRIBIR
    while os.path.exists(f"csv_{funcion_obtener_datos}_limpios_{file_number}.csv"):
        file_number += 1
    filename = f"csv_{funcion_obtener_datos}_limpios_{file_number}.csv" 
    
    df_limpio.to_csv(filename, index=False)
     
    return {"mensaje": f"Datos de {funcion_obtener_datos} limpiados y guardados exitosamente en '{filename}'"}

# EJEMPLO HECHO endpoint_limpiar_dataframe("articles","Unemployement Benefits","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"])

# DIFERENCIA CON LA ANTERIOR VERSION, HEMOS INCLUIDO EL PARAMETRO DESCARGA PARA PODER EVITAR EL PROBLEMA DE LA DESCARGA DOBLE EN EL ENDPOINT FINAL, INCLUIDO LA FECHA DE LOS DATOS QUE QUEREMOS
#Y SACARLOS DE LOS PARAMETROS DE LA API PARA UNA LLAMADA MAS CORTA. TAMBIEN HEMOS CREADO UNA CARPETA PARA CADA UNO DE LOS 3 ENDPOINTS
#Y QUE SUS EXTRACCIONES RESPECTIVAS SE LOCALICEN AHI. 
# PROBLEMA ENCONTRADO: al intentar hacer los mismo con el endpoint de limpieza y crear una carpeta para cada uno,
# SOLO SE ME DESCARGABA LA CARPETA DE ARTICLES, LA PRIMERA.SERA UN PROBLEMA CON EL IF, LO DEJAMOS PARA ARREGLARLO MAÑANA. 