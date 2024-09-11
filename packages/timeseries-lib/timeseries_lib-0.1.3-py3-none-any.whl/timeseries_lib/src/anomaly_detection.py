import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

def detect_anomalies_iqr(series):
    """
    Обнаружение аномалий с использованием межквартильного размаха (IQR)

    series: временной ряд
    """

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    anomalies = series[(series < lower_bound) | (series > upper_bound)]

    return anomalies

def detect_anomalies_z_score(series, threshold=3):
    """
    Обнаружение аномалий с использованием Z-оценки

    series: временной ряд
    threshold: порог для Z-оценки
    """

    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std
    anomalies = series[np.abs(z_scores) > threshold]

    return anomalies


def detect_anomalies_iso_forest(train, test, contamination=0.01, n_estimators=1000, max_samples=1000):
    """
    Обнаружение аномалий с использованием isolation forest

    train: датасет для обучения
    test: датасет для применения
    """
    iso_forest = IsolationForest(contamination=contamination, n_estimators=n_estimators, max_samples=max_samples)
    iso_forest.fit(train)

    predictions = iso_forest.predict(test)

    return predictions == -1


def detect_anomalies_oc_svm(train, test, kernel='rbf', gamma=0.005, nu=0.001):
    """
    Обнаружение аномалий с использованием OneClass SVM

    train: датасет для обучения
    test: датасет для применения
    """
    oc_svm = OneClassSVM(kernel=kernel, gamma=gamma, nu=nu)
    oc_svm.fit(train)

    predictions = oc_svm.predict(test)

    return predictions == -1


def delete_anomalies(series, anomalies):
    """
    Удаление аномалий из временного ряда.

    series: временной ряд (pd.Series или np.array)
    anomalies: аномалии, которые нужно удалить (pd.Series, np.array или list)

    Возвращает временной ряд без указанных аномалий.
    """
    return series[~series.isin(anomalies)]
