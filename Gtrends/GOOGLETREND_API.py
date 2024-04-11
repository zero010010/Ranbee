# el primer end
from pytrends.request import TrendReq
from fastapi import FastAPI
import pandas as pd
import time
import requests



app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my Gtrend_API application!"}

url = 'https://trends.google.com/trends/'
response = requests.get(url, timeout=10)


country_list = ['AT','BE', 'CH', 'DE', 'DK', 'EE', 'GR', 'ES',
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

#ejemplo del uso 

#palabra_clave = "Unemployment"
#datos8 = obtener_datos_google_trends_mensual(palabra_clave)
#atos8



# in case  If it fails , retry with some backoff strategy (e.g., wait 5minutes). if it break  at ' At' reduce countries or ignore the first index in the list  (we can later creat a function) and retry 
# it my  take a time it depends on the topic [18,6s to 8 minutes ]
# if retries > 3 it will break but dont worry  
# wait 10 minutes and retry again 
# the 4th time should work perfectlly 
