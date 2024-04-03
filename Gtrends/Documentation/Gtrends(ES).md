# Descripción de la Aplicación FastAPI para Obtener Datos de Google Trends

## Propósito
Esta aplicación FastAPI sirve como una interfaz para obtener datos de Google Trends para categorías específicas y países. Expone un punto final de API que acepta parámetros de categoría, palabra clave específica (tema) y rango de fechas, y devuelve los datos correspondientes de Google Trends en formato JSON.

## Componentes
1. **Framework FastAPI**: La aplicación está construida utilizando FastAPI, un framework web moderno, rápido (de alto rendimiento) para construir APIs con Python 3.7+.(version utilizada 3.10)

2. **Obtención de Datos de Google Trends**: Utiliza la biblioteca `pytrends`, que proporciona una interfaz para consultar datos de Google Trends. La función `obtener_datos_google_trends_semanal2()` o `obtener_datos_google_trends_semanal2()` es responsable de obtener datos de Google Trends para la categoría, países y rango de fechas especificados. Maneja los errores de manera adecuada y vuelve a intentar la solicitud después de un breve retraso si se produce un error.

3. **Punto Final de API**:

### Punto Final 1: `/google-trends/{tema}`
- **Descripción**: Este punto final permite a los usuarios consultar datos de Google Trends para un tema específico proporcionando el tema como un parámetro de ruta.
- **Método**: GET
- **Parámetros de Ruta**:
  - `{tema}`: Representa el tema para el cual se solicitan los datos de Google Trends.
- **Funcionalidad**:
  - Llama a la función `obtener_datos_google_trends_semanal()` con el tema proporcionado.
  - Convierte el resultado a un diccionario.
  - Devuelve los datos como una respuesta JSON.
- **Uso de Ejemplo**:
  - `GET /google-trends/Beneficios%20de%20Desempleo`

### Punto Final 2: `/google-trends/{categoría}`
- **Descripción**: Este punto final permite a los usuarios consultar datos de Google Trends para una categoría específica proporcionando la categoría como un parámetro de ruta. Los parámetros de consulta adicionales `fecha_inicio` y `fecha_fin` especifican el inicio y el fin del período de fechas para la recuperación de datos.
- **Método**: GET
- **Parámetros de Ruta**:
  - `{categoría}`: Representa la categoría para la cual se solicitan los datos de Google Trends.
- **Parámetros de Consulta**:
  - `fecha_inicio` (opcional): Especifica la fecha de inicio para la recuperación de datos.
  - `fecha_fin` (opcional): Especifica la fecha de finalización para la recuperación de datos.
- **Funcionalidad**:
  - Llama a la función `obtener_datos_google_trends_semanal2()` para obtener los datos para la categoría, fecha de inicio y fecha de finalización proporcionadas.
  - Devuelve los datos como una respuesta JSON.
- **Uso de Ejemplo**:
  - `GET /google-trends/Instalaciones%20Médicas%20y%20Servicios?fecha_inicio=2014-01-01&fecha_fin=2024-03-31`

## Consideraciones
- **Manejo de Errores**: La aplicación maneja los errores durante la obtención de datos, como problemas de red o solicitudes no válidas, imprimiendo mensajes de error y volviendo a intentar la solicitud después de un retraso.
- **Límite de Tasa**: No se implementan mecanismos de límite de tasa explícitos en el código. Dependiendo de los límites de tasa de Google, las solicitudes excesivas pueden resultar en bloqueos o restricciones temporales.
- **Seguridad**: La aplicación no implementa mecanismos de autenticación o autorización. Dependiendo del entorno de implementación y los requisitos, pueden ser necesarias medidas de seguridad adicionales.

## Conclusión
Esta aplicación FastAPI proporciona una forma conveniente de acceder a los datos de Google Trends de forma programática para análisis o integración en otros sistemas. Abstrae la complejidad de la consulta de Google Trends y expone una interfaz de API simple e intuitiva.

## Consideraciones sobre los Países
Los países también fueron verificados manualmente, y hay algunas observaciones sobre algunos países:

- **AT (Austria)**: Se observa que "AT" puede referirse tanto a "Lower Austria" como a "Upper Austria", dependiendo del contexto específico.

- **BE (Bélgica)**

- **CH (Suiza)**

- **CY (Chipre)**

- **CZ (República Checa)**

- **DE (Alemania)**

- **DK (Dinamarca)**

- **EE (Estonia)**

- **GR (Grecia)**

- **ES (España)**

- **FI (Finlandia)**

- **FR (Francia)**

- **HU (Hungría)**

- **IE (Irlanda)**

- **IS (Islandia)**

- **IT (Italia)**

- **LU (Luxemburgo)**

- **ME (Montenegro)**

- **MT (Malta)**

- **NL (Países Bajos)**

- **NO (Noruega)**

- **PL (Polonia)**

- **PT (Portugal)**

- **SE (Suecia)**

- **SI (Eslovenia)** ; not as SL

- **UK (Reino Unido)**: Se refiere a United Kingdom y su código ISO es GB.

- **LV (Letonia)**: También puede representarse como LG.

Es importante tener en cuenta estas observaciones al manejar los códigos de país en el contexto de esta aplicación.
