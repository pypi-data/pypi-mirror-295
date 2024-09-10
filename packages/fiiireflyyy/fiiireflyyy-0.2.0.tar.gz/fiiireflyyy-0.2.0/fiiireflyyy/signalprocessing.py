import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, freqz
from scipy.signal import find_peaks


def butter_filter(signal, order, filt_type, fs, lowcut=None, highcut=None, cut=None, ):
    """
    Filter a signal using a butterworth filter.

    Parameters
    ----------
        signal: Iterable.
            The data to filter.
        order: int
            Order of the filter
        filt_type: ["highpass", "lowpass", "bandstop", "bandpass"]
            Type of the filter.
        fs: int
            Sampling frequency of the signal.
        lowcut: int
            Low cut, if filter type is bandstop or bandpass.
        highcut: int
            High cut, if the filter type is bandstop or bandpass.
        cut: int
            Cut frequency, if the filter type is lowpass or highpass.

    Returns
    -------
        ndarray: Filtered signal

    """
    nyq = 0.5 * fs
    if cut:
        midcut = cut / nyq
    if lowcut:
        low = lowcut / nyq
    if highcut:
        high = highcut / nyq
    if filt_type in ["highpass", "lowpass"]:
        b, a = butter(order, midcut, btype=filt_type)
        w, h = freqz(b, a)
    elif filt_type in ["bandstop", "bandpass"]:
        b, a = butter(order, [low, high], btype=filt_type)
        w, h = freqz(b, a)

    # xanswer = (w / (2 * np.pi)) * freq
    # yanswer = 20 * np.log10(abs(h))

    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal  # , xanswer, yanswer


def fast_fourier(dfy, freq):
    """
    Apply a fast fourier transform on data.
    The second half of the transformed data
    (mirroring) is not returned.

    Parameters
    ----------
        dfy: Iterable
            The signal to transform.
        freq: int
            The sampling frequency.

    Returns
    -------
        tuple
            The power, the frequencies

    """
    fft_df = np.fft.fft(dfy)
    freqs = np.fft.fftfreq(len(dfy), d=1 / freq)

    clean_fft_df = abs(fft_df)
    clean_freqs = abs(freqs[0:len(freqs // 2)])
    return clean_fft_df[:int(len(clean_fft_df) / 2)], clean_freqs[:int(len(clean_freqs) / 2)]


