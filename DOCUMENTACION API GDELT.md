# DOCUMENTACION API PARA GDELT
Para crear una API con la que extraeremos los datos de la plataforma GDELT según unos filtros elegidos, los descargaremos a csv y los limpiaremos para su posterior uso hemos usado FASTAPI, pues es una plataforma con la que estamos familiarizados gracias a The Bridge.

## Descripción
Esta API nos facilitará acceso a datos de GDELT y tendrá endpoints especializados para extraer artículos y obtener el tono y la popularidad de los mismos. De la misma forma, dispondrá de una función de limpieza para los datos obtenidos.
Hemos creado dos versiones de la misma API, una con la funcion de limpieza integrada dentro del endpoint y otra con una llamada independiente para la limpieza final.

## Endpoints
Hemos creado 4 endpoints y una función adicional.

### 1. Obtención de artículos completos
#### @app.get("/articles/")
Este endpoint permite buscar artículos de GDELT según los criterios que hayamos incluido como parametros, así como transformar y descargar en csv esos datos.

#### Parámetros 
- `keyword` (str): Palabra clave para la búsqueda.
- `start_date` (str): Fecha de inicio en formato "YYYY-MM-DD".
- `end_date` (str): Fecha de fin en formato "YYYY-MM-DD".
- `country` (str): País del artículo.

#### Respuestas
- `200 OK`: Los datos se han obtenido correctamente y se ha guardado un archivo CSV en el servidor.
- {"mensaje": "Datos de artículos limpiados y guardados exitosamente"} (Si la función limpiar_dataframe está incluida dentro del mismo endpoint y no en llamada externa)

### 2. Obtención del tono de nuestros artículos
#### @app.get("/tone/")
Este endpoint permite obtener el tono de los artículos de GDELT según los criterios que hemos seleccionado como parámetros.
Nos proporcionará información sobre si el tono es positivo (mayor que 0), negativo (menor que 0) o neutro(0). Igual que en el endpoint anterior, tras extraer los datos nos los descarga en formato csv en nuestro ordenador

#### Parámetros
- `keyword` (str): Palabra clave para la búsqueda.
- `start_date` (str): Fecha de inicio en formato "YYYY-MM-DD".
- `end_date` (str): Fecha de fin en formato "YYYY-MM-DD".
- `country` (str): País del artículo.

#### Respuestas
- `200 OK`: Los datos se han obtenido correctamente y se ha guardado un archivo CSV en el servidor.
- {"mensaje": "Datos de artículos limpiados y guardados exitosamente"} (Si la función limpiar_dataframe está incluida dentro del mismo endpoint y no en llamada externa)

### 3. Obtención de la popularidad de nuestros artículos
#### @app.get("/popularity/")
Este endpoint permite obtener la popularidad de los artículos de GDELT según los criterios seleccionados como parámetros.
Los valores en la columna “Volume Intensity” qe obtenemos de este endpoint pueden variar entre 0 y 1.
Un valor de 0.1839 significa que, en ese intervalo de tiempo, los artículos relacionados con el tema tenían una popularidad relativa del 18.39% en comparación con el total de artículos monitoreados.
Esta llamada también nos permite descargar el csv.

#### Parámetros
- `keyword` (str): Palabra clave para la búsqueda.
- `start_date` (str): Fecha de inicio en formato "YYYY-MM-DD".
- `end_date` (str): Fecha de fin en formato "YYYY-MM-DD".
- `country` (str): País del artículo.

#### Respuestas
- `200 OK`: Los datos se han obtenido correctamente y se ha guardado un archivo CSV en el servidor.
- {"mensaje": "Datos de artículos limpiados y guardados exitosamente"} (Si la función limpiar_dataframe está incluida dentro del mismo endpoint y no en llamada externa)

### 4. Limpieza de los datos de los 3 endpoints anteriores (LLAMADA OPCIONAL, SOLO EN EL CASO QUE NO LO TENGAMOS INCLUIDO DENTRO DE LAS MISMOS ENDPOINTS)
#### @app.get("/limpieza/")
Este endpoint permite limpiar los datos obtenidos de los otros endpoints.

#### Parámetros 
- `funcion_obtener_datos` (str): Nombre de la función de la que se obtienen los datos ("articles", "tone" o "popularity").
- Resto de parámetros dependientes de la función seleccionada (`keyword`,`start_date`,`end_date`,`country`)

#### Respuestas
- `200 OK`: Los datos se han limpiado correctamente y se ha guardado un archivo CSV limpio en el servidor.(SI TENEMOS ENDPOINT DE LIMPIEZA)

### 5. Funciones adicionales
#### Función `limpiar_dataframe`
La utilizaremos para limpiar un DataFrame, eliminando filas con valores nulos y duplicados.
def limpiar_dataframe(df: pd.DataFrame):
    """
    Funcion para limpiar el DataFrame eliminando filas con valores nulos y duplicados.
    Entrada:
        df (pd.DataFrame): El DataFrame a limpiar.   
    Salida:
        pd.DataFrame: El DataFrame limpio.
    """
    df_limpio = df.dropna().drop_duplicates()
    return df_limpio

### NOTA, PODEMOS USAR ESTA FUNCION PARA LIMPIAR UN DATAFRAME CUALQUIERA, NO SOLO PARA ESTOS.
