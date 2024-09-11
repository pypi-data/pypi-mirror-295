import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import sklearn

from app.timeseries_lib import (
    moving_average, exponential_smoothing, savitzky_golay_filter,
    plot_time_series, plot_smoothed_series, plot_anomalies,
    decompose_series, model_forecast,
    detect_anomalies_iqr, detect_anomalies_z_score, detect_anomalies_iso_forest, detect_anomalies_oc_svm,
    ar_model, ma_model, arima_model, sarima_model, holt_winters_model,
    check_stationarity_adf, plot_trend, plot_autocorrelation,
    plot_periodogram, plot_fft
)


data = pd.read_csv("anomalies_dataset.csv")
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

df = data[['Timestamp', 'Давление нагнетания 2-й ступени, кПа_5.5.4', 'Давление азота на ГДК-1, кПа _5.5.6',
           'Давление всасывания ГДК-1, кПа_5.5.4', 'Давление азота СГУ 2-й ст, кПа_5.5.6']].copy()

df = data.set_index('Timestamp')
df = df.resample('1Min').mean()
df.dropna(inplace=True)
df.sort_index(inplace=True)

df['year'] = df.index.year
df['month'] = df.index.month
df['day'] = df.index.day
df['hour'] = df.index.hour
df['minute'] = df.index.minute

train = df[df.index < '2024-02-01']

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train)
df_scaled = scaler.transform(df)

# Обнаружение аномалий с помощью isolation forest
anomalies = detect_anomalies_iso_forest(train_scaled, df_scaled)
df['Anomaly ISOF'] = anomalies
df_anomalies = df[df['Anomaly ISOF']]

# Вывод графика с аномалиями
plot_anomalies(df['Давление азота СГУ 2-й ст, кПа_5.5.6'], df_anomalies['Давление азота СГУ 2-й ст, кПа_5.5.6'],
               title='Anomalies detected using Isolation Forest')

# Обнаружение аномалий с помощью OneClass SVM
anomalies = detect_anomalies_oc_svm(train_scaled, df_scaled)
df['Anomaly OCSVM'] = anomalies
df_anomalies = df[df['Anomaly OCSVM']]

# Вывод графика с аномалиями
plot_anomalies(df['Давление азота СГУ 2-й ст, кПа_5.5.6'], df_anomalies['Давление азота СГУ 2-й ст, кПа_5.5.6'],
               title='Anomalies detected using OneClass SVM')
