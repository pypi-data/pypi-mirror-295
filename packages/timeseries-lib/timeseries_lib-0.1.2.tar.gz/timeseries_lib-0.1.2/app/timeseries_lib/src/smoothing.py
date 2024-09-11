from scipy.signal import savgol_filter

def moving_average(series, window):
    """
    Сглаживание методом скользящего среднего

    series: временной ряд
    window: размер окна скользящего среднего
    """

    return series.rolling(window=window).mean()

def exponential_smoothing(series, alpha):
    """
    Экспоненциальное сглаживание

    series: временной ряд
    alpha: коэффициент сглаживания (от 0 до 1)
    """

    return series.ewm(alpha=alpha).mean()

def savitzky_golay_filter(series, window_length, polyorder):
    """
    Фильтр Савицкого-Голея

    series: временной ряд
    window_length: длина окна
    polyorder: порядок полинома
    """

    return savgol_filter(series, window_length, polyorder)
