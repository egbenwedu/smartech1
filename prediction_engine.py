import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def train_model():
    # This trains the model using the data you generated
    df = pd.read_csv('adsorbent_data.csv')
    X = df[['amine_loading', 'surface_area', 'humidity', 'temp']]
    y = df['capacity']
    model = RandomForestRegressor()
    model.fit(X, y)
    joblib.dump(model, 'smartech1_adsorbent_model.pkl')
    return "Model trained!"

def predict_capacity(amine, area, hum, temp):
    # If the model file is missing, train it first
    if not os.path.exists('smartech1_adsorbent_model.pkl'):
        train_model()
    
    # Load the model and make the prediction
    model = joblib.load('smartech1_adsorbent_model.pkl')
    result = model.predict([[amine, area, hum, temp]])
    return round(result[0], 4)