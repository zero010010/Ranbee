from fastapi import FastAPI
from gdeltdoc import GdeltDoc, Filters
import pandas as pd
import os

app = FastAPI()

# 3 ENDPOINTS PARA EXTRAER DATOS DE GDELT y uno para la limpieza 
@app.get("/articles/") 
def get_articles(keyword: str, start_date: str, end_date: str, country: str):
    f = Filters(keyword=keyword,
        start_date=start_date,
        end_date=end_date,
        country=country)
    gd = GdeltDoc()
    articles = gd.article_search(f)
    df = pd.DataFrame(articles)
    file_number = 1  # Comprobamos si el archivo ya existe CON EL BUCLE WHILE, para evitar que se sobreescriban los archivos
    while os.path.exists(f"csv_articulos_{file_number}.csv"):
        file_number += 1
    filename = f"csv_articulos_{file_number}.csv"
    df.to_csv(filename, index=False) # si lo que queremos es que se nos descargue en el ordenador y obtener un mensaje de que se ha hecho bien
    return df # lo hemos cambiado, para obtener un df!!! que antes con el 200:ok la funcion de limpieza no funcionaba

# EJEMPLO PRUEBA REALIZADA print(get_articles("Inclusive growth","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"]))

@app.get("/tone/") # PARA EL TONO, hemos modificado 
def get_tone_results(keyword: str, start_date: str, end_date: str, country: str):
    f = Filters(keyword=keyword,
        start_date=start_date,
        end_date=end_date,
        country=country)
    gd = GdeltDoc()
    tone_results = gd.timeline_search("timelinetone", f)
    df_tono = pd.DataFrame(tone_results)
    file_number = 1  # Comprobamos si el archivo ya existe CON EL BUCLE WHILE, para evitar que se sobreescriban los archivos
    while os.path.exists(f"csv_tono_{file_number}.csv"):
        file_number += 1
    filename = f"csv_tono_{file_number}.csv"
    df_tono.to_csv(filename, index=False)
    return df_tono # Lo cambiamos para obtener un df que podamos usar en la funcion de limpieza

# Ejemplo prueba print(get_tone_results("Inclusive growth","2018-05-10","2023-05-11",["Austria","Belgium","Switzerland","Cyprus","Germany","Denmark","Estonia","Spain"]))

@app.get("/popularity/") # PARA LA POPULARIDAD
# Funcion popularidad, mismo cambio para que no se sobreescriban que en las anteriores
def get_popularity_results(keyword: str, start_date: str, end_date: str, country: str):
    f = Filters( keyword=keyword,
        start_date=start_date,
        end_date=end_date,
        country=country)
    gd = GdeltDoc()
    popularity_results = gd.timeline_search("timelinevol", f)
    df_popularidad = pd.DataFrame(popularity_results)
    file_number = 1  # Comprobamos si el archivo ya existe CON EL BUCLE WHILE
    while os.path.exists(f"csv_popularidad_{file_number}.csv"):
        file_number += 1
    filename = f"csv_popularidad_{file_number}.csv"
    df_popularidad.to_csv(filename, index=False)
    
    return df_popularidad # lo cambiamos para obtener un df que podamos usar en la funcion de limpieza
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
def endpoint_limpiar_dataframe(funcion_obtener_datos: str, keyword: str, start_date: str, end_date: str, country: str): # LOS PARAMETROS NECESARIOS
    if funcion_obtener_datos == "articles":
        df = get_articles(keyword, start_date, end_date, country)
    elif funcion_obtener_datos == "tone":
        df = get_tone_results(keyword, start_date, end_date, country)
    elif funcion_obtener_datos == "popularity":
        df = get_popularity_results(keyword, start_date, end_date, country)
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

# ASI SE DESCARGAN TANTO UN CSV LIMPIO COMO UNO SUCIO, AL USAR LAS LLAMADAS GET ARTICLES, GET TONE Y GET POPULARITY, LA DESCARGA
# DEL CSV SUCEDE IGUAL. PREGUNTAR SI DEBERIAMOS CREAR UN NUEVO ENDPOINT QUE NO DESCARGUE EL ARCHIVO SUCIO, SI NO SOLO EL DF!!