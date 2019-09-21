import wfdb
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from IPython.display import display
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


string='chfdb/chf00'
record = [[] for i in range(15)]
signal = [[] for i in range(15)]
for i in range(15):
    new= string.split("f")
    if int(new[2])<9:
        string_2 = new[:2] + list(str(0))
        string_3 = list("f".join(str(e) for e in string_2[:3])) +  list(str(int(new[2])+1))
        string = "".join(str(e) for e in string_3)
    else:
        string_2 = new[:2] +  list(str(int(new[2])+1))
        string_3 = list("f".join(str(e) for e in string_2[:3])) + list(string_2[3]) 
        string = "".join(str(e) for e in string_3)
    print(string)

    record[i]=wfdb.rdsamp(string,sampto=1000)
    signal[i]=record[i].p_signals
    #wfdb.plotrec(record[i], title=string)

data=[]

for i in range(len(signal[1])):
    data.append(signal[1][i][0])




#LP Butterworth_filter
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='bandpass', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# LPF 
order = 6
fs=250
cutoff = 3.667

b, a = butter_lowpass(cutoff, fs, order)

w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

         
n = len(signal[0]) # total number of samples
T = n/fs
t = np.linspace(0, T, n, endpoint=False)

#data = signal[0]

y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
