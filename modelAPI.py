from fastapi import FastAPI
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import classification_report
import pickle

app = FastAPI()

@app.get("/setupv0")
def setup_api():
    """
    Función que hace el setup desde el historico, separa en train y test
    """
    df_EUROSTAT = pd.read_csv("EUROSTAT/data/serie/serie.csv")
    df_GTREND = pd.read_csv('GTrends/data/final/gtrend.csv')
    df_GDELT = pd.read_csv('GDELT/data/final/gdelt.csv')
    
    data = pd.concat([df_GTREND, df_GDELT], axis=1)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    train_data, test_data = train_test_split(data, test_size=0.2, shuffle=False)  # No barajar para mantener la temporalidad

    scaler = MinMaxScaler()
    train_data_scaled = scaler.fit_transform(train_data)
    test_data_scaled = scaler.transform(test_data)

    # Definir el número de pasos de tiempo (timesteps) y características (features)
    n_timesteps = # Define el número de pasos de tiempo
    n_features = 24 # Define el número de características

    # Preparar datos de entrenamiento y prueba en el formato adecuado para LSTM
    def prepare_data(data, n_timesteps):
        X, y = [], []
        for i in range(len(data) - n_timesteps):
            X.append(data[i:i + n_timesteps, :])
            y.append(data[i + n_timesteps, :])
        return np.array(X), np.array(y)

    train_X, train_y = prepare_data(train_data_scaled, n_timesteps)
    test_X, test_y = prepare_data(test_data_scaled, n_timesteps)

    # Construir el modelo LSTM
    model = Sequential([
    LSTM(units=50, activation='relu', input_shape=(n_timesteps, n_features)),
    Dense(data.shape[1])  # La capa de salida tiene el mismo número de características que las series temporales originales
    ])
    model.compile(optimizer='adam', loss='mse')

    # Entrenar el modelo
    model.fit(train_X, train_y, epochs=100, batch_size=32, validation_split=0.2)
    
    with open('model/lstm.pkl', 'wb') as archivo:
        pickle.dump(model, archivo)
    
    return classification_report(y_test, predicciones_tree)   


@app.get("/headserie")
def head_api():
    """
    Función muestra el head de serie EUROSTAT
    """
    df = pd.read_csv("EUROSTAT/data/serie/serie_EU.csv")
    df_ = df.head(5)
    return json.loads(df_.to_json(orient='records'))


   


@app.post("/predict/{paciente}")
def predict_api(paciente):
    """
    Función que predice para un paciente dado
    """
    scaler = MinMaxScaler()
    paciente_scaled = scaler.fit_transform(paciente)
    with open("model/lstm.pkl", 'rb') as archivo:
        modelo_cargado = pickle.load(archivo)
    #cargar modelo
    return modelo_cargado.predict(paciente_scaled)

@app.get("/v1/metrics")
def metrics_api():
    """
    Función que muestra las metricas del modelo
    """
    x_train_scaled = pd.read_csv("data/processed/x_train.csv")
    y_train = pd.read_csv("data/processed/y_train.csv")
    x_test_scaled = pd.read_csv('data/processed/x_test.csv')
    y_test = pd.read_csv('data/processed/y_test.csv')

    with open("model/lstm.pkl", 'rb') as archivo:
        modelo_cargado = pickle.load(archivo)
    
    modelo_cargado.fit(x_train_scaled,y_train)
    predicciones_tree = modelo_cargado.predict(x_test_scaled)
    
    return classification_report(y_test, predicciones_tree)
