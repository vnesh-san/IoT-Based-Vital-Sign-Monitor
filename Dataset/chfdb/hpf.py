import wfdb
import numpy as np
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

#Main Program
if __name__=="__main__":

    string='chfdb/chf00'
    record = [[] for i in range(15)]
    sig = [[] for i in range(15)]
    data = [[] for i in range(15)]
    fourier_sig = [[] for i in range(15)]
    cwt_sig = [[] for i in range(15)]

        
    order = 6
    fs=250
    cutoff = 3.667

    x=[]
    b, a = butter_highpass(cutoff, fs, order)

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
        sig[i]=record[i].p_signals
        #wfdb.plotrec(record[i], title=string)

        #for j in range(len(sig[i])):
            #data[i].append(sig[i][j][0])
        mini=x.append(len(sig[i]))
        
        n = len(sig[i]) # total number of samples
        T = n/fs
        t = np.linspace(0, T, n, endpoint=False)


        # HPF 

        y = butter_highpass_filter(data[i], cutoff, fs, order)

        #Just because the below lines are hashed, don't delete it !!! 

        w, h = freqz(b, a, worN=8000)
        plt.subplot(2, 1, 1)
        plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
        plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
        plt.axvline(cutoff, color='k')
        plt.xlim(0, 0.5*fs)
        plt.title("HPF Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()

        
        plt.subplot(2, 1, 2)
        plt.plot(t, data[i], 'b-', label='data = %s' % string)
        plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
        plt.xlabel('Time [sec]')
        plt.grid()
        plt.legend()
        plt.subplots_adjust(hspace=0.35)
        plt.show()

        
        #FFT
        #fourier_sig[i]=fft(y)
        #xf = np.linspace(0.0, 1.0/(2.0*T), n//2)
        #plt.plot(xf, 2.0/n * np.abs(fourier_sig[i][0:n//2]))
        #plt.grid()
        #plt.show()

        #CWT
        #widths = np.arange(1, 31)
        #cwt_sig[i] = cwt(y, signal.ricker, widths)
        #plt.imshow(cwt_sig, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto', vmax=abs(cwt_sig).max(), vmin=-abs(cwt_sig).max())
        #plt.show()
