import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz, cwt
from scipy.fftpack import fft
from scipy import signal

#HP Butterworth_filter
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


sig=pd.read_csv('ECG5000.csv')
sig=np.array(sig)
        
order = 6
fs=250
cutoff = 3.667


b, a = butter_highpass(cutoff, fs, order)

n = len(sig[1])-1 # total number of samples
T = n/fs
t = np.linspace(0, T, n, endpoint=False)

data=sig[2][:140]

# HPF 

y = butter_highpass_filter(data, cutoff, fs, order)
plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()
