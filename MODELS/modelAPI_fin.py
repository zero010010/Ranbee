# url = 'http://127.0.0.1:8000/setupv0?red=yes or no
# url = 'http://127.0.0.1:8000/v1/train?model="random"or"xgboost"or"lstm"&red=yes or no
# url = 'http://127.0.0.1:8000/v1/metrics?model="random"or"xgboost"or"lstm"&red=yes or no
# url = 'http://127.0.0.1:8000/v1/predict?model="random"or"xgboost"or"lstm"&red="yes" or "no"&DICCIONARIO CON LOS DATOS A PREDECIR
# url = http://127.0.0.1:8000/docs PARA LA ORGANIZACION
# url = 'http://127.0.0.1:8000/v1/predict?model=random&red=no&data=0,0.18800292611558156,0.8007448789571692,0.8626760563380282,0.5468164794007492,0.08638360175695461,0.21814254859611237,0.35119047619047616,0.8007448789571692,0.8626760563380282,0.5468164794007492,0.08638360175695461,0.21814254859611237,0.35119047619047616,0.3685106382978691,0.2064220183486662,0.4118895966029621,0.09144551263600234,0.12853107344632816,0.5345285524568394,0.536531057927362,0.5435265033145533,1.0,0.831334645341426,0.5553603225473825,0.6842047996977231,0.21945866861741048,0.09656181419166066,0.08412582297000726,0.6052141527001864,0.32588454376163867,0.5046554934823093,1.0000000000000002,0.8186619718309858,0.8433098591549297,0.5318352059925094,0.4775280898876405,0.3857677902621724,0.060029282576866766,0.07027818448023426,0.057101024890190345,0.1936645068394528,0.08999280057595394,0.10583153347732177,0.0,0.5952380952380952,0.0,0.6052141527001864,0.32588454376163867,0.5046554934823093,1.0000000000000002,0.8186619718309858,0.8433098591549297,0.5318352059925094,0.4775280898876405,0.3857677902621724,0.060029282576866766,0.07027818448023426,0.057101024890190345,0.1936645068394528,0.08999280057595394,0.10583153347732177,0.0,0.5952380952380952,0.0,0.43744680851063866,0.22042553191489003,0.3123404255319161,0.3623853211009182,0.20183486238530823,0.4403669724770442,0.42250530785562257,0.1910828025477684,0.39490445859871326,0.07466467100339613,0.026193080421391846,0.09107132577283947,0.18008474576270078,0.11581920903954343,0.15536723163841878,0.36188579017264055,0.07990261177512159,0.3760513501549353,0.6727720936126899,0.5324640468878707,0.5923625592828305,0.699007512231563,0.5752800165001182,0.6357946245620701,0.7927313995286758,0.41381035640980696,0.6323306964210081,0.807588060072711,0.8814650290932436,0.7879865003079789,0.6760692236731287,0.48445567707060994,0.29741445829991336,0.5557465001110798,0.35333563073219976,0.5775363370948867
# OJO, EL PREDICT ES UNA LLAMADA POST
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Request
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
def setup_api(red: str): # SI RED ES SI, SE HACER SELECKT BEST, SI NO NO
    """
    Función que hace el setup desde el historico, separa en train y test
    Parametros de entrada: red, str, para elegir la opcion de reducir la dimensionalidad con selectkbest o no
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
    
    if red.lower() == "yes": # revisar esto, no se descarga, ME FALTABAN LOS PARENTESIS!!! PATETICO JAJAJAJAAJ
        X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)
        pd.DataFrame(X_train).to_csv('X_train_reduce.csv')
        pd.DataFrame(X_test).to_csv('X_test_reduce.csv')
        pd.DataFrame(y_train).to_csv('y_train_reduce.csv')
        pd.DataFrame(y_test).to_csv('y_test_reduce.csv')   
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        pd.DataFrame(X_train).to_csv('X_train.csv')
        pd.DataFrame(X_test).to_csv('X_test.csv')
        pd.DataFrame(y_train).to_csv('y_train.csv')
        pd.DataFrame(y_test).to_csv('y_test.csv')
        return "The data has been split into training and testing sets and saved to CSV files successfully"
        
        
@app.get("/v1/train")
def train(model: str,red: str):
    """Función para entrenar el modelo. Carga los datos para entrenar el modelo,
    y, una vez hecho, guarda EL MODELO en tu ordenador, su ruta y las metricas del modelo. 
    Input: model,str, para seleccionar el modelo elegido y red,str, para confirmar si se usa selecktbest o no
    Output: dict: JSON con las metricas del modelo y la ruta donde se ha guardado"""        
    if red.lower() == "yes":
        X_train_reduce = pd.read_csv('X_train_reduce.csv')
        y_train_reduce = pd.read_csv('y_train_reduce.csv')
        y_test_reduce = pd.read_csv('y_test_reduce.csv')
        X_test_reduce = pd.read_csv('X_test_reduce.csv')     
    else:
        X_train = pd.read_csv('X_train.csv')
        y_train = pd.read_csv('y_train.csv')
        y_test = pd.read_csv('y_test.csv')
        X_test = pd.read_csv('X_test.csv')
    
    if model.lower() == "lstm": # a pesar de estar arriba especificado, volvemos a poner aqui, la lectura
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
        return "Model downloaded in pickle format"

    if model.lower() == "random": 
        if red == "yes":     
            rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_regressor.fit(X_train_reduce, y_train_reduce)
            with open('random_red.pkl', 'wb') as f:
                pickle.dump(rf_regressor, f) # IMPORTANTE!!! GUARDAMOS COMO MODEL EN LUGAR DE GUARDAR EL MODELO
            print("Model downloaded in pickle format")
            
        else:
            rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_regressor.fit(X_train, y_train)
            with open('random.pkl', 'wb') as f:
                pickle.dump(rf_regressor, f)
            return "Model downloaded in pickle format"
    
    if model.lower() == "xgboost":
        if red == "yes":
            xgb_regressor = xgb.XGBRegressor(objective ='reg:squarederror', n_estimators=100, random_state=42)
            xgb_regressor.fit(X_train_reduce, y_train_reduce)
            with open('XGBOOST_red.pkl', 'wb') as f: 
                pickle.dump(xgb_regressor, f)
            print("Model downloaded in pickle format")
        else:
            xgb_regressor = xgb.XGBRegressor(objective ='reg:squarederror', n_estimators=100, random_state=42)
            xgb_regressor.fit(X_train, y_train)
            with open('XGBOOST.pkl', 'wb') as f: 
                pickle.dump(xgb_regressor, f)
            return "Model downloaded in pickle format"
        
@app.get("/v1/metrics")
def metrics(model:str,red:str):
    """Función para obtener las métricas del modelo. Carga el modelo ya entrenado, carga los datos de test y devuelve el clasification report.
    Input: model, str, con el nombre del modelo y red, str, con una respuesta de yes o no.
    Output: dict: JSON con el classification report del modelo"""
    if red.lower() == "yes":
        y_test_reduce = pd.read_csv('y_test_reduce.csv')
        X_test_reduce = pd.read_csv('X_test_reduce.csv')
            
    else:
        y_test = pd.read_csv('y_test.csv')
        X_test = pd.read_csv('X_test.csv')
    
    if model.lower() == "lstm":
        with open('LSTM.pkl', 'rb') as f:
            model = pickle.load(f)
        y_pred = model.predict(X_test_reduce)
        mse = mean_squared_error(y_test_reduce, y_pred)
        r2 = r2_score(y_test_reduce, y_pred)
        return {"Mean Squared Error": mse, "R-squared": r2}
    
    elif model.lower() == "random":
        if red.lower() == "yes":
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
    
    elif model.lower() == "xgboost":
        if red.lower() == "yes":
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
@app.post("/predict") # creamos una llamada nueva, derivada de la anterior, pero no funciona tampoco
async def predict(request: Request):
    try:
        data = await request.json()
        model = data.get("model")
        red = data.get("red")
        datos = data.get("data")

        if model.lower() == "lstm":
            with open('LSTM.pkl', 'rb') as f:
                model = pickle.load(f)
            prediction = model.predict([datos])[0]
            return {"prediction": prediction}
        elif model.lower() == "random":
            if red.lower() == "yes":
                with open('random_red.pkl', 'rb') as f:
                    model = pickle.load(f)
                prediction = model.predict([datos])[0]
                return {"prediction": prediction}
            else:
                with open('random.pkl', 'rb') as f:
                    model = pickle.load(f)
                prediction = model.predict([datos])[0]
                return {"prediction": prediction}
        elif model.lower() == "xgboost":
            if red.lower() == "yes":
                with open('XGBOOST_red.pkl', 'rb') as f:
                    model = pickle.load(f)
                prediction = model.predict([datos])[0]
                return {"prediction": prediction}
            else:
                with open('XGBOOST.pkl', 'rb') as f:
                    model = pickle.load(f)
                prediction = model.predict([datos])[0]
                return {"prediction": prediction}
        else:
            raise HTTPException(status_code=400, detail="Unsupported model")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
@app.get("/v1/predict")
def predict(model: str, red: str, datos: list): # probamos con una lista, porque le diccionario no funciona
    """Función para obtener predicción. Carga el modelo, llama a la función predict del modelo pasándole los datos que le has pasado a la llamada. 
    Input: model:str, para seleccionar el modelo, red:str, para elegir con SELECKTBEST O NO, list: lista con los valores de las variables predictoras, para nuestra prueba.
    Output: dict: JSON con la predicción."""
    if model.lower() == "lstm":
        with open('LSTM.pkl', 'rb') as f:
            model = pickle.load(f)
        prediccion = model.predict([datos])[0]
        return {"prediccion": prediccion}
    elif model.lower() == "random":
        if red.lower() == "yes":
            with open('random_red.pkl', 'rb') as f:
                model = pickle.load(f)
            prediccion = model.predict([datos])[0]
            return {"prediccion": prediccion}
        else:
            with open('random.pkl', 'rb') as f:
                model = pickle.load(f)
            prediccion = model.predict([datos])[0]
            return {"prediccion": prediccion}
    elif model.lower() == "xgboost":
        if red.lower() == "yes":
            with open('XGBOOST_red.pkl', 'rb') as f:
                model = pickle.load(f)
            prediccion = model.predict([datos])[0]
            return {"prediccion": prediccion}
        else:
            with open('XGBOOST.pkl', 'rb') as f:
                model = pickle.load(f)
            prediccion = model.predict([datos])[0]
            return {"prediccion": prediccion}
    else: 
        return {"Error": "Unsupported model"}
    