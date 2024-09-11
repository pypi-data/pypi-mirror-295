import matplotlib.pyplot as plt

def plot_time_series(series, title='Time Series'):
    """
    Построение графика временного ряда

    series: временной ряд
    title:  заголовок графика
    """

    plt.figure(figsize=(10, 6))
    plt.plot(series, label='Original Series')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

def plot_smoothed_series(original_series, smoothed_series, title='Smoothed Series'):
    """
    Построение графика сглаженного временного ряда

    original_series: исходный временной ряд
    smoothed_series: сглаженный временной ряд
    title:  заголовок графика
    """

    plt.figure(figsize=(10, 6))
    plt.plot(original_series, label='Original Series')
    plt.plot(smoothed_series, label='Smoothed Series', color='red')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

def plot_anomalies(series, anomalies, title='Anomalies in Time Series'):
    """
    Построение графика временного ряда с выделением аномалий

    series: временной ряд
    anomalies: временной ряд аномалий
    title:  заголовок графика
    """

    plt.figure(figsize=(10, 6))
    plt.plot(series, color='blue', label='Time Series')
    plt.scatter(anomalies.index, anomalies, color='red', label='Anomalies')
    plt.legend(loc='best')
    plt.title(title)
    plt.show()