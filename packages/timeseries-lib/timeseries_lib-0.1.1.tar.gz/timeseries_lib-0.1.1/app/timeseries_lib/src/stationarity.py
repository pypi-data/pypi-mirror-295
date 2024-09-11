from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

def check_stationarity_adf(series, alpha=0.05):
    """
    Проверка стационарности временного ряда с помощью теста Дики-Фуллера

    series: временной ряд
    alpha: порог для отвержения нулевой гипотезы
    """

    result = adfuller(series)
    p_value = result[1]
    is_stationary = p_value < alpha

    return {
        'Test Statistic': result[0],
        'p-value': p_value,
        'Lags Used': result[2],
        'Number of Observations Used': result[3],
        'Critical Values': result[4],
        'Is Stationary': is_stationary
    }

def plot_trend(series, period):
    """
    Построение тренда временного ряда

    series: временной ряд
    period: размер окна
    """

    rolling_mean = series.rolling(window=period).mean()
    rolling_std = series.rolling(window=period).std()

    plt.figure(figsize=(10, 6))
    original = plt.plot(series, color='blue', label='Original')
    mean = plt.plot(rolling_mean, color='red', label='Rolling Mean')
    std = plt.plot(rolling_std, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

def plot_autocorrelation(series, lags=50):
    """
    Построение автокорреляции временного ряда

    series: временной ряд
    lags: количество лагов
    """

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(series, lags=lags, ax=ax[0])
    plot_pacf(series, lags=lags, ax=ax[1])
    plt.show()

def differentiate_series(series, period=1):
    """
    Дифференцирование временного ряда.

    series (pd.Series): Временной ряд.
    period (int): Период дифференцирования.

    pd.Series: Временной ряд после дифференцирования.
    """
    differentiated_series = series.diff(period)

    return differentiated_series

def make_series_stationary(series):
    """
    Приведение временного ряда к стационарному.

    series (pd.Series): Исходный временной ряд.

    """
    # Логарифмирование для стабилизации дисперсии
    log_series = np.log(series)

    # Вычитание скользящего среднего для удаления тренда
    moving_avg = log_series.rolling(window=12).mean()
    log_series_minus_moving_avg = log_series - moving_avg
    log_series_minus_moving_avg.dropna(inplace=True)

    # Дифференцирование для того, чтобы ряд стал стационарным
    stationary_series = log_series_minus_moving_avg.diff().dropna()

    return stationary_series

