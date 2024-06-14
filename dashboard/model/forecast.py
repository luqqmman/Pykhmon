import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

from django.conf import settings

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def predict_next_year():
    model = load_model(settings.SALES_MODEL_PATH)
    sales_data = pd.read_csv(settings.CSV_PATH, parse_dates=True, index_col='date')
    sales_data.drop(['customer'], axis=1, inplace=True)

    full_scaler = MinMaxScaler()
    scaled_full_data = full_scaler.fit_transform(sales_data)

    forecast = []
    periods = 12
    length = 10
    n_features = 1

    first_eval_batch = scaled_full_data[-length:]
    current_batch = first_eval_batch.reshape((1, length, n_features))

    for i in range(periods):
        current_pred = model.predict(current_batch)[0]
        forecast.append(current_pred)
        current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)

    forecast = full_scaler.inverse_transform(forecast)


    forecast_index = pd.date_range(start=pd.Timestamp("today").strftime("%Y-%m-%d"), periods=periods, freq='MS')
    forecast_data = pd.DataFrame(data=forecast, index=forecast_index, columns=['Forecast'])
    

    data = [d[0] for d in model.predict(forecast_data)]
    x = [months[index.month-1] for index in forecast_index]

    plt.figure(figsize=(10, 6))
    plt.plot(x, data, marker='o', linestyle='-', color='b')

    # Menambahkan judul dan label
    plt.title('Forecast for the Next Year')
    plt.xlabel('Month')
    plt.ylabel('Rupiah')

    # Menampilkan grid
    plt.grid(True)

    # Menampilkan plot
    plt.savefig(settings.SALES_FORECAST_PATH)
    return data


def predict_customer():
    model = load_model(settings.CUSTOMER_MODEL_PATH)
    sales_data = pd.read_csv(settings.CSV_PATH, parse_dates=True, index_col='date')
    sales_data.drop(['profit'], axis=1, inplace=True)

    with open(settings.CUSTOMER_SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    forecast_start_date = '2024-06-14'
    forecast_start_date = pd.Timestamp("today").strftime("%Y-%m-%d")
    periods = 12
    length = 10
    n_features = 1

    last_data = sales_data[-length:]
    scaled_last_data = scaler.transform(last_data)
    input_data = []

    for i in range(periods):
        if i == 0:
            current_batch = scaled_last_data.reshape((1, length, n_features))
        else:
            current_batch = np.append(current_batch[:,1:,:], [[pred]], axis=1)

        pred = model.predict(current_batch)[0]
        input_data.append(pred)

    forecast = scaler.inverse_transform(input_data)
    forecast_index = pd.date_range(start=forecast_start_date, periods=periods, freq='D')
    forecast_data = pd.DataFrame(forecast, index=forecast_index, columns=['Forecast'])
    predictions_array = forecast_data['Forecast'].values


    x = [days[index.day-1] for index in forecast_index]

    print("Forecast Data:")
    print(forecast_data)
    print("\nPredictions Array (for backend):")
    print(predictions_array)

    plt.figure(figsize=(10, 6))
    plt.plot(x, predictions_array, marker='o', linestyle='-', color='b')

    # Menambahkan judul dan label
    plt.title('Customer Forecast')
    plt.xlabel('Day')
    plt.ylabel('Customer')

    # Menampilkan grid
    plt.grid(True)

    # Menampilkan plot
    plt.savefig(settings.CUSTOMER_FORECAST_PATH)
    return forecast_data
