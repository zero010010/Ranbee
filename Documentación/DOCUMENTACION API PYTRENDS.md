# DOCUMENTACION API PARA GOOGLE TRENDS

Para crear una API con la que extraeremos los datos de la plataforma Google Trend, usando como base la API no oficial PYTRENDS, su descarga en formato csv y un preprocesamiento para su posterior uso hemos usado FASTAPI, pues es una plataforma con la que estamos familiarizados gracias a The Bridge.

## Descripción

Esta API nos facilitará acceso a datos de GOOGLE TRENDS con la API no oficial de Pytrends y tendrá endpoints especializados para extraer la media de las búsquedas de un tópico definido en un tiempo determinado. En un primer momento, hemos creado los endpoints con datos de fecha y países ya definidos, PERO NO DESCARTAMOS INCLUIR EN LOS PARÁMETROS DE LAS LLAMADAS O DE LA FUNCION CREADA PARA LA EXTRACCIÓN LOS PAÍSES O FECHAS QUE NECESITEMOS, ESTUDIAREMOS CUÁL ES LA MEJOR OPCIÓN. Hemos creado dos versiones de la misma API, una con la función de limpieza integrada dentro de cada endpoint y otra con una llamada independiente para la limpieza final.

## Endpoints

Hemos creado 2 endpoints (UNO OPCIONAL) y 2 funciones adicionales.

### 1. Obtención de datos de búsqueda con GOOGLE TRENDS

#### @app.get("/google-trends/{topic}") 

Este endpoint permite obtener los datos de interés de las búsquedas según el tópico que hayamos incluido como parámetro, así como transformar y descargar en csv esos datos.

#### Parámetros 

- `topic` (str): El tema o término de búsqueda para el cual se desea obtener datos de Google Trends.
- `category` (str, opcional): La categoría a la que pertenece el tópico de búsqueda en Google Trends.

#### Respuestas

- `200 OK`: Los datos se han obtenido correctamente y se ha guardado un archivo CSV en el servidor.
- {"mensaje": "Datos de Trends limpiados y guardados exitosamente"} (en el caso de que la llamada a la función de limpieza se haga dentro de este endpoint)

### 2. Limpieza de los datos (LLAMADA OPCIONAL, SOLO EN EL CASO QUE NO LO TENGAMOS INCLUIDO DENTRO DEL MISMO ENDPOINT)

#### @app.get("/limpieza/")

Este endpoint permite limpiar los datos obtenidos de los otros endpoints.

#### Parámetros 

- `topic` (str): El tema o término de búsqueda para el cual se desea limpiar y guardar los datos de Google Trends.

#### Respuestas

- `200 OK`: Los datos se han limpiado correctamente y se ha guardado un archivo CSV limpio en el servidor (SI TENEMOS ENDPOINT DE LIMPIEZA).

### 3. Funciones adicionales

#### Función `limpiar_dataframe`

La utilizaremos para limpiar un DataFrame, eliminando filas con valores nulos y duplicados.

```python
def limpiar_dataframe(df: pd.DataFrame):
    """
    Función para limpiar el DataFrame eliminando filas con valores nulos y duplicados.
    Entrada:
        df (pd.DataFrame): El DataFrame a limpiar.
    Salida:
        pd.DataFrame: El DataFrame limpio.
    """
    df_limpio = df.dropna().drop_duplicates()
    return df_limpio

### NOTA, ES IMPORTANTE EN AMBAS APIS QUE TENGAMOS EN CUENTA QUE LAS LLAMADAS Y LOS CSV CORRESPONDIENTES NO SE SOBREESCRIBAN AL HACER VARIAS LLAMADAS (TIMESTAMP?), NO SE SI AHORA LO HACEN, HAY QUE MIRARLO.
### También hay que revisar que los datos que obtenemos son mensuales, no semanales, pues los semanales se vuelven nulos.!!
