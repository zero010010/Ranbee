# Documentación del código de extracción de datos de GDELT

## Descripción
Esta documentación explica el uso de la librería gdeltdoc de Python para realizar consultas filtradas a la API de GDELT y analizar los datos recuperados.<br>

Se detalla cómo configurar filtros de búsqueda por palabras clave, fechas y países para consultar artículos y eventos relacionados. También se documenta el procesamiento de los resultados en DataFrames de Pandas, analizando campos como el tono y la popularidad de los artículos a lo largo del tiempo.<br>

El objetivo es proveer una guía paso a paso para extraer y analizar datos relevantes de la base GDELT de una manera eficiente y reproducible. Los ejemplos concretos facilitan la adaptación del código a distintos casos de uso.


## Importación de Librerías
 
 
Se importan las librerías gdeltdoc y pandas que se utilizarán en el código. gdeltdoc provee funcionalidades para consultar la base de datos GDELT, pandas se utilizará para manejar los datos extraídos en DataFrames.

## Configuración de filtros

Se crea un objeto Filters de gdeltdoc para definir los filtros de búsqueda:

**keyword**: Palabra clave a buscar en los artículos. Por ejemplo: "sustainability", "economic crisis", etc.
En este caso "Inclusive growth".<br>

**start_date y end_date**: Rango de fechas para filtrar los artículos. De 2018-05-10 a 2023-05-11.

**country**: Lista de países para filtrar los artículos. Se han especificado varios países de Europa. Se pueden especificar hasta 9 países simultáneamente. Por ejemplo: ["ESP", "DEU", "FRA"].


**Código de los paises:**

AT: Austria<br>
BE: Belgium<br>
CH: Switzerland<br>
CY: Cyprus<br>
CZ: Czech Republic<br>
DE: Germany<br>
DK: Denmark<br>
EE: Estonia<br>
EL: Greece<br>
ES: Spain<br>
FI: Finland<br>
FR: France<br>
HU: Hungary<br>
IE: Ireland<br>
IS: Iceland<br>
IT: Italy<br>
LU: Luxembourg<br>
ME: Montenegro<br>
MT: Malta<br>
NL: Netherlands<br>
NO: Norway<br>
PL: Poland<br>
PT: Portugal<br>
SE: Sweden<br>
SI: Slovenia<br>
UK: United Kingdom<br>
LT: Lithuania<br>
LV: Latvia<br>

Además de los filtros de keyword, fecha y país, gdeltdoc  permite configurar otros filtros para las consultas a la API de GDELT:<br>

**sourcecountry**: Filtrar por país de la fuente/medio de comunicación.<br>

**sourceurl**: Filtrar por URL específica de un medio.<br>

**language:** Filtrar por idioma.<br>


**inurl:** Buscar una palabra clave en la URL del artículo.<br>

**intitle:** Buscar en el título del artículo.<br>

**summary:** Buscar en el resumen del artículo.<br>

**eventactiongeo_country:** Filtrar eventos por país donde ocurrieron.<br>

**eventactiongeo_lat y eventactiongeo_long:** Filtrar por coordenadas geográficas.<br>

Y algunos más que se pueden consultar en la documentación de gdeltdoc. Esto permite configurar consultas específicas. Se pueden combinar múltiples filtros simultáneamente para obtener datos relevantes.<br>



## Consulta de artículos<br>

Primero creamos un objeto GdeltDoc sin pasarle filtros.<br>

Luego se llama al método *article_search *pasándole el objeto Filters creado previamente.<br>

Esto realiza la consulta a la API de GDELT aplicando los filtros definidos y devuelve los resultados como una lista de diccionarios. <br>

##  Conversión a DataFrame<br>

Para facilitar el análisis, se convierte la lista de diccionarios a un DataFrame de Pandas con pd.DataFrame().
Esto permite manipular los datos en forma de tabla con las funciones de Pandas. <br>
El DataFrame resultante tendrá una fila por cada artículo recuperado y columnas para todos los campos de los diccionarios. De esta manera se pueden analizar fácilmente los artículos filtrados por los criterios especificados.<br>


##  Análisis del tono <br>

Para analizar el tono (positivo/negativo) de los artículos sobre el tema consultado se utiliza el método *timeline_search() *. Se pasa como primer parámetro "timelinetone" para indicar que queremos obtener datos de tono.<br>

Y como segundo parámetro se vuelve a pasar el objeto Filters con los criterios de búsqueda. Esto devuelve un DataFrame de Pandas con las siguientes columnas:<br>

* **date:** Fecha del artículo<br>
* **tone:** Tono promedio del artículo en esa fecha<br>

Los valores de la columna tone indican:

* **Valores cercanos a 0**: artículos con tono neutro.<br>
* **Valores positivos**: artículos con tono positivo.<br>
* **Valores negativos:** artículos con tono negativo.<br>

De esta manera podemos analizar como fluctúa el tono de los artículos sobre el tema consultado a lo largo del tiempo basados en nuestros filtros, asi obtenemos una visión del sentimiento positivo/negativo en la cobertura mediática del tema.

## Análisis de popularidad

Al igual que con el tono, se utiliza timeline_search() para obtener datos de popularidad.

Se pasa **"timelinevol"** como primer parámetro para indicar popularidad, esto devuelve un DataFrame con las columnas:<br>

* **date:** Fecha del intervalo<br>
* **volume_intensity:** Popularidad del tema en ese intervalo<br>

**Interpretación de la popularidad**<br>

La popularidad mide la cantidad de menciones de un tema en los artículos. Los valores en *volume_intensity *representan la popularidad relativa en un intervalo de tiempo específico.


**Rango de valores**<br>

Los valores de *volume_intensity* pueden variar entre 0 y 1.<br>

Por ejemplo, 0.1839 significa que en ese intervalo los artículos sobre el tema tenían una popularidad relativa del 18.39% con respecto al total de artículos.






