
import os
from pytrends.request import TrendReq
from fastapi import FastAPI
import pandas as pd
import time
import requests

from fastapi.responses import RedirectResponse



app = FastAPI()

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

url = 'https://trends.google.com/trends/'
response = requests.get(url, timeout=10)


country_list = ['BE', 'CH', 'DE', 'DK', 'EE', 'GR', 'ES',
       'FI', 'FR', 'HU', 'IE', 'IS', 'IT','LU', 'ME',
       'MT', 'NL', 'NO', 'PL', 'PT', 'SE', 'SI','GB',
        'LT', 'LV']


def obtener_datos_google_trends_mensual(palabra_clave, paises=country_list, fecha_inicio='2014-01-01', fecha_fin='2024-03-31'):
    try:
        pytrends = TrendReq(hl='es', tz=360)
        trends_data = {}
        for pais in paises:
            try:
                pytrends.build_payload(kw_list=[palabra_clave], timeframe=f'{fecha_inicio} {fecha_fin}', geo=pais)
                data = pytrends.interest_over_time()
                if data.empty:
                    raise ValueError(f"No hay datos disponibles para la palabra clave y país '{pais}'.")
                data_mensual = data.resample('M').mean()
                trends_data[pais] = data_mensual.to_dict()
            except Exception as e:
                print(f"Error al obtener datos de Google Trends para el país '{pais}': {e}")
                # Break off the loop if an error occurs for a country
                break
        return trends_data
    except Exception as e:
        print(f"Error al obtener datos de Google Trends: {e}")
        time.sleep(60)
        return obtener_datos_google_trends_mensual(palabra_clave, paises, fecha_inicio, fecha_fin)

@app.get("/google-trends/{topic}")
def google_trends_handler(topic: str, fecha_inicio: str = '2014-01-01', fecha_fin: str = '2024-03-31'):
    trends_data = obtener_datos_google_trends_mensual(topic, country_list, fecha_inicio, fecha_fin)
    return trends_data


@app.get("/save-csv/{topic}")
def save_csv_handler(topic: str):
    
        # Obtain data
        datos = obtener_datos_google_trends_mensual(topic)

        # Convert data to DataFrame
        df = pd.DataFrame.from_dict({(i, j): datos[i][j] 
                                      for i in datos.keys() 
                                      for j in datos[i].keys()},
                                     orient='index')

        # Create directory if it doesn't exist
        directory = 'data'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save DataFrame as CSV
        df.to_csv(os.path.join(directory, f'datos_{topic}.csv'), index=True, encoding='utf-8')
        
        return {"message": f"CSV file for '{topic}' saved successfully"}

# para la limpieza we will use the same endpoints of gdelt that is  what we agreed on with the team


















#ejemplo del uso 

palabra_clave = "Unemployment"
#datos8 = obtener_datos_google_trends_mensual(palabra_clave)
#atos8



# in case  If it fails , retry with some backoff strategy (e.g., wait 5minutes). if it break  at ' At' reduce countries or ignore the first index in the list  (we can later creat a function) and retry 
# it my  take a time it depends on the topic [18,6s to 8 minutes ]
# if retries > 3 it will break but dont worry  
# wait 10 minutes and retry again 
# the 4th time should work perfectlly 
