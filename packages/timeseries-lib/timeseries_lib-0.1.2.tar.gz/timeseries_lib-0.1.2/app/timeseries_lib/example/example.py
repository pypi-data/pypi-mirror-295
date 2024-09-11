import pandas as pd
import matplotlib.pyplot as plt
from app.timeseries_lib import (
    moving_average, exponential_smoothing, savitzky_golay_filter,
    plot_time_series, plot_smoothed_series, plot_anomalies,
    decompose_series, model_forecast,
    detect_anomalies_iqr, detect_anomalies_z_score,
    ar_model, ma_model, arima_model, sarima_model, holt_winters_model,
    check_stationarity_adf, plot_trend, plot_autocorrelation,
    plot_periodogram, plot_fft
)

# Создаем пример временного ряда
data = pd.read_csv('Airplane.csv', parse_dates=['Date'])
time_series = data.groupby('Date')['Fatalities'].sum()

# Сглаживание
smoothed_ma = moving_average(time_series, window=12)
smoothed_es = exponential_smoothing(time_series, alpha=0.3)
smoothed_sg = savitzky_golay_filter(time_series, window_length=11, polyorder=2)

# Визуализация
plot_time_series(time_series, title='Airplane Crashes Fatalities')
plot_smoothed_series(time_series, smoothed_ma, title='Moving Average Smoothing')
plot_smoothed_series(time_series, smoothed_es, title='Exponential Smoothing')
plot_smoothed_series(time_series, smoothed_sg, title='Savitzky-Golay Smoothing')

# Проверка стационарности
stationarity_result = check_stationarity_adf(time_series)
print('ADF Test Result:')
print(stationarity_result)

# Построение тренда
period = 12
plot_trend(time_series, period)

# Построение автокорреляции
plot_autocorrelation(time_series)

# Декомпозиция
decomposition = decompose_series(time_series)
decomposition.plot()
plt.show()

# Спектральный анализ
plot_periodogram(time_series)
plot_fft(time_series)

# Обнаружение аномалий
anomalies_iqr = detect_anomalies_iqr(time_series)
print('Anomalies detected using IQR method:')
print(anomalies_iqr)

anomalies_z_score = detect_anomalies_z_score(time_series)
print('Anomalies detected using Z-score method:')
print(anomalies_z_score)

# Визуализация аномалий
plot_anomalies(time_series, anomalies_iqr, title='Anomalies (IQR method)')
plot_anomalies(time_series, anomalies_z_score, title='Anomalies (Z-score method)')

# Моделирование
ar_fit = ar_model(time_series, lags=5)
print(ar_fit.summary())

ma_fit = ma_model(time_series, lags=5)
print(ma_fit.summary())

arima_fit = arima_model(time_series, order=(1, 1, 1))
print(arima_fit.summary())

sarima_fit = sarima_model(time_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
print(sarima_fit.summary())

holt_winters_fit = holt_winters_model(time_series, seasonal_periods=12)
print(holt_winters_fit.summary())

# Прогнозирование
forecast_ar = model_forecast(ar_fit, steps=10)
print('\nAR forecast')
print(forecast_ar)

forecast_ma = model_forecast(ma_fit, steps=10)
print('\nMA forecast')
print(forecast_ma)

forecast_arima = model_forecast(arima_fit, steps=10)
print('\nARIMA forecast')
print(forecast_arima)

forecast_sarima = model_forecast(sarima_fit, steps=10)
print('\nSARIMA forecast')
print(forecast_sarima)

forecast_holt_winters = model_forecast(arima_fit, steps=10)
print('\nHolt-Winters forecast')
print(forecast_holt_winters)