from fastapi import FastAPI
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import r2_score
import pickle
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import os
import requests

app = FastAPI()

@app.get("/setupv0")
def setup_api(reduce: str): # SI REDUCE ES SI, SE HACER SELECKT BEST, SI NO NO
    """
    Función que hace el setup desde el historico, separa en train y test
    Parametros de entrada: reduce, str, para elegir la opcion de reducir la dimensionalidad con selectkbest o no
    Salida: str, confirmando que se han descargado los csv de x_train, x_test y_train e y_test.
    """
    df_EUROSTAT = pd.read_csv("EUROSTAT/data/serie/serie_EU.csv")
    df_GTREND = pd.read_csv('GTrends/data/final/gtrend_monthly_2017.csv')
    df_GDELT = pd.read_csv('GDELT/data/final/gdelt_monthly.csv')
    data = pd.concat([df_GTREND, df_GDELT], axis=1)
    data.drop("Media",axis=1, inplace=True)
    data = data.set_index("Date")
    index_original = data.index # OJO, HACEMOS ESTO PORQUE LUEGO AL MONTAR LAGGED DATA EL INDICE SE PIERDE, COMPROBADO AL ESCALAR
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    # Preparamos los datos con lag
    lag_steps = 3
    lagged_data = pd.DataFrame(scaled_data,index=index_original,columns=data.columns) # uno nuevo con los datos escalados, PERO OJO, NO TIENE INDICE
    for column in lagged_data.columns:
    # Aplicar lag desplazando cada columna hacia abajo por el número de pasos de tiempo especificado
        for step in range(1, lag_steps + 1):
            lagged_data[f"{column}_lag{step}"] = lagged_data[column].shift(step) # si lo quisieramos para arriba, -step
        
    # y eliminamos las 3 primeras columnas con nulo (o lo sustituimos), consultar
    lagged_data.dropna(inplace=True)
    # IMPORTANTE, PLANTEARNOS SI SUBIR o bajar en las fechas, preguntar a los profes!!!
    X = lagged_data.values
    # Y PARA LA Y, Cambiamos el nombre de la columna "year_month" a "Date", para que se llame como las de X
    df_EUROSTAT.rename(columns={'year_month': 'Date'}, inplace=True)
    df_EUROSTAT['Date'] = pd.to_datetime(df_EUROSTAT['Date'])
    df_EUROSTAT.set_index('Date', inplace=True)

    # Rellenamos los valores faltantes de los meses anteriores con el mes siguiente
    df_EUROSTAT_RES = df_EUROSTAT.resample('M').ffill()
    df_EUROSTAT_RES
    # Plantearnos si es mejor el bfill hasta enero en lugar de ir para abajo, pues de las otras series tenemos datos
    # hasta enero, preguntar profes
    # para evitar  incongruencia con la X (al hacer el lag eliminamos las 3 primeras filas) y una de ellas era coincidente con y
    # eliminamos la fila 1 de y, SOLO DE MOMENTO, CONSULTAREMOS MAÑAÑA
    df_EUROSTAT_RES = df_EUROSTAT_RES.iloc[1:]
    y = df_EUROSTAT_RES["total"].values
    # PARA REDUCIR LA DIMENSIONALIDAD PROBAMOS SELECTKBEST (reduce columnas)
    selector = SelectKBest(score_func=f_regression, k=27)  # he puesto 27, porque es lo que nos salio en pca, para probar, podriamos cambiarlas
    selector.fit(X, y)
    X_selected = selector.transform(X)
    selected_features = selector.get_support() # para elegir las caracteristicas seleccionadas
    # luego filtrar las caracteristicas
    X_selected = X[:, selected_features]
    
    if reduce.lower == "yes":
        X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)
        pd.DataFrame(X_train).to_csv('X_train_reduce.csv')
        pd.DataFrame(X_test).to_csv('X_test_reduce.csv')
        pd.DataFrame(y_train).to_csv('y_train_reduce.csv')
        pd.DataFrame(y_test).to_csv('y_test_reduce.csv')
        return "The data has been split into training and testing sets and saved to CSV files successfully"
    
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        pd.DataFrame(X_train).to_csv('X_train.csv')
        pd.DataFrame(X_test).to_csv('X_test.csv')
        pd.DataFrame(y_train).to_csv('y_train.csv')
        pd.DataFrame(y_test).to_csv('y_test.csv')
        return "The data has been split into training and testing sets and saved to CSV files successfully"
        
        
@app.get("/v1/train") # revisar si funcionan las metricas asi, si no eliminar llamada interna y meter todo en setup
def train(model: str,reduce: str):
    """Función para entrenar el modelo. Carga los datos para entrenar el modelo,
    y, una vez hecho, guarda EL MODELO en tu ordenador, su ruta y las metricas del modelo. 
    Input: ninguno
    Output: dict: JSON con las metricas del modelo y la ruta donde se ha guardado"""        
    if reduce == "yes":
        X_train_reduce = pd.read_csv('X_train_reduce.csv')
        y_train_reduce = pd.read_csv('y_train_reduce.csv')
        y_test_reduce = pd.read_csv('y_test_reduce.csv')
        X_test_reduce = pd.read_csv('X_test_reduce.csv')
            
    else:
        X_train = pd.read_csv('X_train.csv')
        y_train = pd.read_csv('y_train.csv')
        y_test = pd.read_csv('y_test.csv')
        X_test = pd.read_csv('X_test.csv')
    
    if model.lower == "lstm": # a pesar de estar arriba especificado, volvemos a poner aqui, la lectura
        # SOLO EN ESTE CASO, porque no aceptaría un NO en reduce, Y POR SI EL CLIENTE LO INTRODUCE POR ERROR
        X_train = pd.read_csv('X_train_reduce.csv')
        y_train = pd.read_csv('y_train_reduce.csv')
        y_test = pd.read_csv('y_test_reduce.csv')
        X_test = pd.read_csv('X_test_reduce.csv')
    
        lag_steps = 3
        n_features = 9 # Son las features que encajan con la dimensionalidad (64x3x9) para 1728 
        # Reformateamos los datos para que sean 3D (número de muestras, número de pasos de tiempo, número de características)
        X_train = X_train.reshape(X_train.shape[0], lag_steps, n_features)
        X_test = X_test.reshape(X_test.shape[0], lag_steps, n_features)
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(lag_steps, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=20, batch_size=8, validation_data=(X_test, y_test))
        with open('LSTM.pkl', 'wb') as f:
            pickle.dump(model, f)
        metrics_response = requests.get('http://127.0.0.1:8000/v1/metrics') #Para obtener métricas del otro endpoint
        metrics = metrics_response.json()
        response = {"metrics": metrics,
            "model_path": os.path.abspath('LSTM.pkl')}
        return response

    if model.lower == "random": 
        if reduce == "yes":     
            rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_regressor.fit(X_train_reduce, y_train_reduce)
            with open('random_red.pkl', 'wb') as f:
                pickle.dump(model, f)
            metrics_response = requests.get('http://127.0.0.1:8000/v1/metrics') #Para obtener métricas del otro endpoint
            metrics = metrics_response.json()
            response = {"metrics": metrics,
                "model_path": os.path.abspath('random.pkl')}
            return response
        else:
            rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_regressor.fit(X_train, y_train)
            with open('random.pkl', 'wb') as f:
                pickle.dump(model, f)
            metrics_response = requests.get('http://127.0.0.1:8000/v1/metrics') #Para obtener métricas del otro endpoint
            metrics = metrics_response.json()
            response = {"metrics": metrics,
                "model_path": os.path.abspath('random.pkl')}
            return response
    
    if model.lower == "xgboost":
        if reduce == "yes":
            xgb_regressor = xgb.XGBRegressor(objective ='reg:squarederror', n_estimators=100, random_state=42)
            xgb_regressor.fit(X_train_reduce, y_train_reduce)
            with open('XGBOOST_red.pkl', 'wb') as f: 
                pickle.dump(model, f)
            metrics_response = requests.get('http://127.0.0.1:8000/v1/metrics') #Para obtener métricas del otro endpoint
            metrics = metrics_response.json()
            response = {"metrics": metrics,
                "model_path": os.path.abspath('XGBOOST.pkl')}
            return response
        else:
            xgb_regressor = xgb.XGBRegressor(objective ='reg:squarederror', n_estimators=100, random_state=42)
            xgb_regressor.fit(X_train, y_train)
            with open('XGBOOST.pkl', 'wb') as f: 
                pickle.dump(model, f)
            metrics_response = requests.get('http://127.0.0.1:8000/v1/metrics') #Para obtener métricas del otro endpoint
            metrics = metrics_response.json()
            response = {"metrics": metrics,
                "model_path": os.path.abspath('XGBOOST.pkl')}
            return response
        
@app.get("/v1/metrics")
def metrics(model:str,reduce:str):
    """Función para obtener las métricas del modelo. Carga el modelo ya entrenado, carga los datos de test y devuelve el clasification report.
    Input: model, str, con el nombre del modelo y reduce, str, con una respuesta de yes o no.
    Output: dict: JSON con el classification report del modelo"""
    if reduce == "yes":
        y_test_reduce = pd.read_csv('y_test_reduce.csv')
        X_test_reduce = pd.read_csv('X_test_reduce.csv')
            
    else:
        y_test = pd.read_csv('y_test.csv')
        X_test = pd.read_csv('X_test.csv')
    
    if model.lower == "lstm":
        with open('LSTM.pkl', 'rb') as f:
            model = pickle.load(f)
        y_pred = model.predict(X_test_reduce)
        mse = mean_squared_error(y_test_reduce, y_pred)
        r2 = r2_score(y_test_reduce, y_pred)
        return {"Mean Squared Error": mse, "R-squared": r2}
    
    elif model.lower == "random":
        if reduce == "yes":
            with open('random_red.pkl', 'rb') as f:
                model = pickle.load(f)
            y_pred = model.predict(X_test_reduce)
            mse = mean_squared_error(y_test_reduce, y_pred)
            r2 = r2_score(y_test_reduce, y_pred)
            return {"Mean Squared Error": mse, "R-squared": r2}
        else:
            with open('random.pkl', 'rb') as f:
                model = pickle.load(f)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            return {"Mean Squared Error": mse, "R-squared": r2}
    
    elif model.lower == "xgboost":
        if reduce == "yes":
            with open('XGBOOST_red.pkl', 'rb') as f:
                model = pickle.load(f)
            y_pred = model.predict(X_test_reduce)
            mse = mean_squared_error(y_test_reduce, y_pred)
            r2 = r2_score(y_test_reduce, y_pred)
            return {"Mean Squared Error": mse, "R-squared": r2}
        else:
            with open('XGBOOST.pkl', 'rb') as f:
                model = pickle.load(f)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            return {"Mean Squared Error": mse, "R-squared": r2}
        
@app.post("/v1/predict")
def predict(model:str, reduce: str, data: dict):
    """Función para obtener prediccion. Carga el modelo, llama a la función predict del modelo pasandole los datos que le has pasado a la llamada. 
    Input: dict: diccionario con los nombres y valores de las variables predictoras, paa nuestra prueba.
    Output: dict: JSON con la predicción."""
    if model.lower == "lstm":
        with open('LSTM.pkl', 'rb') as f:
            model = pickle.load(f)
        data_values = [data[key] for key in data]
        prediccion = model.predict([data_values])[0]
        return {"prediccion": prediccion} # para que devuelva un json o diccionario
    elif model.lower == "random":
        if reduce == "yes":
            with open('random_red.pkl', 'rb') as f:
                model = pickle.load(f)
            data_values = [data[key] for key in data]
            prediccion = model.predict([data_values])[0]
            return {"prediccion": prediccion} # para que devuelva un json o diccionario
        else:
            with open('random.pkl', 'rb') as f:
                model = pickle.load(f)
            data_values = [data[key] for key in data]
            prediccion = model.predict([data_values])[0]
            return {"prediccion": prediccion} # para que devuelva un json o diccionario
            
    elif model.lower == "xgboost":
        if reduce == "yes":
            with open('XGBOOST_red.pkl', 'rb') as f:
                model = pickle.load(f)
            data_values = [data[key] for key in data]
            prediccion = model.predict([data_values])[0]
            return {"prediccion": prediccion} # para que devuelva un json o diccionario
        else:
            with open('XGBOOST.pkl', 'rb') as f:
                model = pickle.load(f)
            data_values = [data[key] for key in data]
            prediccion = model.predict([data_values])[0]
            return {"prediccion": prediccion} # para que devuelva un json o diccionario
    
    else: 
        return {"Error": "Unsupported model"}
        
        
