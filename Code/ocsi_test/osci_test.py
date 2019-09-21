import serial
import time
import numpy as np
import csv
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

timeout = time.time() + 2*60
file_name='sample.csv'

ser=serial.Serial()
ser.port='COM3'
ser.baudrate=115200
ser.timeout=1
ser.flowrate=None
ser.parity='N'
ser.bytesize=8

ser.open()

data_ecg=[]
data_spo2=[]
dataset=[]

i=0
j=0
flag=0

start_ecg = b'ECG 4Bytes and Respiration 4Bytes:\r\n'
start_spo2 = b'SpO2:\r\n'


class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 1.1)
        self.ax.set_xlim(0, self.maxt)

    def update(self, data_ecg):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def emitter(p=0.03):
    'return a random value with probability p, else 0'
    while True:
        v = np.random.rand(1)
        if v > p:
            yield 0.
        else:
            yield np.random.rand(1)

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
scope = Scope(ax)

while(1):
    x = ser.readline()
    #time.sleep(1)

    if time.time() > timeout:
        break
    if (x==start_ecg or flag==1) and i<=8:
        flag=1
        if (i>=1):
            x=str(x)
            new=x.split("\\r")
            new1=new[0].split("'")
            data_ecg.append(round((3.3 / 1023 )* int(new1[1]),4))
            ani = animation.ArtistAnimation(fig, scope.update, emitter, interval=10,
                              blit=True)

            plt.show()
        i+=1
        j=0
        print(x)
        
    if (x==start_spo2 or flag==2) and j<=3:
        flag=2
        if (j>=1):
            x=str(x)
            new=x.split("\\r")
            new1=new[0].split("'")
            data_spo2.append(int(new1[1]))
        i=0
        j+=1
        print(x)
        
ser.close()

p=0
q=0
for yin in range(min(int(len(data_ecg)/8),int(len(data_spo2)/3))):
    datax=[]
    for yang in range(p,p+8):
        datax.append(data_ecg[yang])
    for yang in range(q,q+3):
        datax.append(data_spo2[yang])
    dataset.append(datax)
    p+=8
    q+=3
    
with open(file_name,'w+',newline='') as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(dataset)

