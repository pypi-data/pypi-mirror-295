import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import periodogram


def plot_periodogram(series, fs=1.0):
    """
    Построение периодограммы для спектрального анализа временного ряда

    series: временной ряд
    fs: частота дискретизации
    """

    freqs, spectrum = periodogram(series, fs=fs)

    plt.figure(figsize=(10, 6))
    plt.plot(freqs, spectrum)
    plt.xlabel('Frequency')
    plt.ylabel('Power Spectrum')
    plt.title('Periodogram')
    plt.show()


def plot_fft(series):
    """
    Построение спектра Фурье для временного ряда

    series: временной ряд
    """
    n = len(series)
    fft_result = np.fft.fft(series)
    fft_freqs = np.fft.fftfreq(n)

    plt.figure(figsize=(10, 6))
    plt.plot(fft_freqs[:n // 2], np.abs(fft_result)[:n // 2])
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.title('Fourier Transform')
    plt.show()
