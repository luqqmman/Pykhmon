import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from django.conf import settings

def predict_next_year():
    model = load_model(settings.MODEL_PATH)
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
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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
    plt.savefig(settings.FORECAST_PATH)
    return data