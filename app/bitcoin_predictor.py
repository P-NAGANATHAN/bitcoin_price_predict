import psycopg2
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

#PostgreSQL
def fetch_data_from_postgres():
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="bitcoin",
        user="bitcoin_usr",
        password="bitcoin_pwd"
    )
    query = """
    SELECT timestamp, buy_price, sell_price, volume
    FROM bitcoin_data
    ORDER BY timestamp DESC
    """
    data = pd.read_sql(query, conn)
    conn.close()
    
    return data

#LSTM
def preprocess_data(data):
    try:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True)
        
        data = data[['buy_price', 'sell_price', 'volume']]

        
        #Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)

        sequence_length = min(60, len(scaled_data)) #At least 60 points for training
        
        if len(scaled_data) < sequence_length:
            raise ValueError(f"Not enough points")
        
        #Sequences
        X, y = [], []
        for i in range(sequence_length, len(scaled_data)):
            X.append(scaled_data[i-sequence_length:i])
            y.append(scaled_data[i, 0])  
        
        X, y = np.array(X), np.array(y)
        
        print(f"Taille de X: {X.shape}, Taille de y: {y.shape}")
        X = np.reshape(X, (X.shape[0], X.shape[1], 3))  
        
        return X, y, scaler
    
    except Exception as e:
        print(f"Erreur lors du prétraitement des données : {str(e)}")
        raise

#LSTM
def train_lstm(X, y):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))  
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))  
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, batch_size=64, epochs=10)
    model.save("/app/bitcoin_price_lstm_model.h5")
    
    return model

#Predict
def predict_bitcoin_price(model, data, scaler):
    last_data = data[-len(data):]  
    last_data_scaled = scaler.transform(last_data)
    
    X_test = []
    X_test.append(last_data_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 3))
    
    predicted_price = model.predict(X_test)
    predicted_price = scaler.inverse_transform([[predicted_price[0][0], 0, 0]])[0][0]
    
    return predicted_price

#Main
def main():
    try:
        data = fetch_data_from_postgres()
        X, y, scaler = preprocess_data(data)
        model = train_lstm(X, y)
        predicted_price = predict_bitcoin_price(model, data[['buy_price', 'sell_price', 'volume']], scaler)
        print(f"Predicted price : {predicted_price}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
