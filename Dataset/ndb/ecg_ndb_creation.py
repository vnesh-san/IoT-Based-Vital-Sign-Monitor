import numpy as np
import csv
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

if __name__=='__main__':
        
        string ='0.csv'
        dataset = []
        x=[]
        z=0
        order = 6
        fs=250
        cutoff = 3.667
        b, a = butter_highpass(cutoff, fs, order)

        for i in range(10):
                x=0
                string_2 = list(string)
                #print(string_2)
                string_2[0]=int(string_2[0])+1
                string = ''.join(str(e) for e in string_2)
                #print(string)
                sig = pd.read_csv(string, usecols = [1])
                sig = np.array(sig)

                n = len(sig[i]) # total number of samples
                T = n/fs
                t = np.linspace(0, T, n, endpoint=False)


                # HPF 
                data = butter_highpass_filter(sig, cutoff, fs, order)
                
                for j in range(int(len(data)/1024)):
                        datax=[]
                        for k in range(x,x+1024):
                                datax.append(int(data[k])/1000)
                        dataset.append(datax)
                        x+=1024
        with open('ecg_ndb_dataset.csv','w+',newline='') as my_csv:
               csvWriter = csv.writer(my_csv,delimiter=',')
               csvWriter.writerows(dataset)
