import wfdb
import numpy as np
import csv
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



if __name__=="__main__":

    string='chfdb/chf00'
    dataset = []
    order = 6
    fs=250
    cutoff = 3.667

    xf=[]
    b, a = butter_highpass(cutoff, fs, order)
    
    for i in range(1,16):
        x=0
        y=1024
        new= string.split("f")
        if int(new[2])<9:
            string_2 = new[:2] + list(str(0))
            string_3 = list("f".join(str(e) for e in string_2[:3])) +  list(str(int(new[2])+1))
            string = "".join(str(e) for e in string_3)
        else:
            string_2 = new[:2] +  list(str(int(new[2])+1))
            string_3 = list("f".join(str(e) for e in string_2[:3])) + list(string_2[3]) 
            string = "".join(str(e) for e in string_3)
        #print(string)



        # HPF 

        for j in range(500):
            record = wfdb.rdsamp(string,sampfrom=x,sampto=y)
            sig = record.p_signals
            


            sig_1 = butter_highpass_filter(sig, cutoff, fs, order)

            n = len(sig) # total number of samples
            T = n/fs
            t = np.linspace(0, T, n, endpoint=False)

            data=[]
            data_1=[]
            
            for k in range(1024):
                data.append(sig[k][0])
                data_1.append(sig_1[k][0])
            x=x+1024
            y=y+1024

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
            plt.plot(t, data, 'b-', label='data = %s' % string)
            plt.plot(t, data_1, 'g-', linewidth=2, label='filtered data')
            plt.xlabel('Time [sec]')
            plt.grid()
            plt.legend()
            plt.subplots_adjust(hspace=0.35)
            plt.show()
            
            dataset.append(np.array(data))

    dataset=np.array(dataset)

    #with open('ecg_dataset_chf.csv','w+',newline='') as my_csv:
     #   csvWriter = csv.writer(my_csv,delimiter=',')
      #  csvWriter.writerows(dataset)


     
        
