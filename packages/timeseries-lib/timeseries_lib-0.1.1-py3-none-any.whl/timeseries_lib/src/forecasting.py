def model_forecast(model_fit, steps=5):
    """
    Прогнозирование временного ряда с использованием модели

    model_fit: обученная модель
    steps: количество шагов для прогноза
    """

    forecast = model_fit.forecast(steps=steps)

    return forecast
