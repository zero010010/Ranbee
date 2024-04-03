# Description of FastAPI Application for Retrieving Google Trends Data

## Purpose
This FastAPI application serves as an interface for retrieving Google Trends data for specific categories and countries. It exposes an API endpoint that accepts category and specific keyword (topic) and date range parameters and returns the corresponding Google Trends data in a JSON format.

## Components
1. **FastAPI Framework**: The application is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.
   
2. **Google Trends Data Retrieval**: It utilizes the `pytrends` library, which provides an interface for querying Google Trends data. The function `obtener_datos_google_trends_semanal2()`o`obtener_datos_google_trends_semanal2()` is responsible for fetching Google Trends data for the specified category, countries, and date range. It handles errors gracefully and retries the request after a brief delay if an error occurs.

3. **API Endpoint**:

### Endpoint 1: `/google-trends/{topic}`
- **Description**: This endpoint allows users to query Google Trends data for a specific topic by providing the topic as a path parameter.
- **Method**: GET
- **Path Parameters**:
  - `{topic}`: Represents the topic for which Google Trends data is requested.
- **Functionality**:
  - Calls the `obtener_datos_google_trends_semanal()` function with the provided topic.
  - Converts the result to a dictionary.
  - Returns the data as a JSON response.
- **Example Usage**:
  - `GET /google-trends/Unemployment%20benefits`

### Endpoint 2: `/google-trends/{category}`
- **Description**: This endpoint allows users to query Google Trends data for a specific category by providing the category as a path parameter. Additional query parameters `fecha_inicio` and `fecha_fin` specify the start and end dates for the data retrieval.
- **Method**: GET
- **Path Parameters**:
  - `{category}`: Represents the category for which Google Trends data is requested.
- **Query Parameters**:
  - `fecha_inicio` (optional): Specifies the start date for the data retrieval.
  - `fecha_fin` (optional): Specifies the end date for the data retrieval.
- **Functionality**:
  - Calls the `obtener_datos_google_trends_semanal2()` function to fetch the data for the provided category, start date, and end date.
  - Returns the data as a JSON response.
- **Example Usage**:
  - `GET /google-trends/Medical%20Facilities%20&%20Services?fecha_inicio=2014-01-01&fecha_fin=2024-03-31`


## Considerations
- **Error Handling**: The application handles errors during data retrieval, such as network issues or invalid requests, by printing error messages and retrying the request after a delay.
- **Rate Limiting**: There are no explicit rate-limiting mechanisms implemented in the code. Depending on Google's rate limits, excessive requests may result in temporary blocks or restrictions.
- **Security**: The application does not implement authentication or authorization mechanisms. Depending on the deployment environment and requirements, additional security measures may be necessary.

## Conclusion
This FastAPI application provides a convenient way to access Google Trends data programmatically for analysis or integration into other systems. It abstracts away the complexity of querying Google Trends and exposes a simple and intuitive API interface.

## Country Considerations
The countries were also manually checked, and there are some remarks about certain countries:

- **AT (Austria)**: It is noted that "AT" can refer to both "Lower Austria" and "Upper Austria," depending on the specific context.

- **BE (Belgium)**

- **CH (Switzerland)**

- **CY (Cyprus)**

- **CZ (Czech Republic)**

- **DE (Germany)**

- **DK (Denmark)**

- **EE (Estonia)**

- **GR (Greece)**

- **ES (Spain)**

- **FI (Finland)**

- **FR (France)**

- **HU (Hungary)**

- **IE (Ireland)**

- **IS (Iceland)**

- **IT (Italy)**

- **LU (Luxembourg)**

- **ME (Montenegro)**

- **MT (Malta)**

- **NL (Netherlands)**

- **NO (Norway)**

- **PL (Poland)**

- **PT (Portugal)**

- **SE (Sweden)**

- **SI (Slovenia)**: not as SL 

- **UK (United Kingdom)**: Refers to the United Kingdom, and its ISO code is GB.

- **LV (Latvia)**: Can also be represented as LG.

It's important to consider these remarks when handling country codes in the context of this application.
