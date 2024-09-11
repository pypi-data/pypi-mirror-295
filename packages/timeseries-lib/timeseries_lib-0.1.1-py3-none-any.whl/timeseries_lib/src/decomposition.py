from statsmodels.tsa.seasonal import seasonal_decompose

def decompose_series(series, model='additive', period=12):
    """
    Декомпозиция временного ряда

    series: временной ряд
    model: тип модели (additive или multiplicative)
    period: период сезонности
    """

    decomposition = seasonal_decompose(series, model=model, period=period)

    return decomposition


