import numpy as np
import pandas as pd
from biosppy.signals import ecg
from sklearn.svm import OneClassSVM
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
chfdb=pd.read_csv("ecg_dataset_chf.csv")
ndb=pd.read_csv("ecg_dataset_ndb.csv")



chfdb=np.array(chfdb)
ndb=np.array(ndb)
chfdb_labels=[[1] for i in range(len(chfdb))]
ndb_labels=[[2] for j in range(len(ndb))]

data_features=[]
data_labels=[]

for i in range(len(chfdb)):
    data_features.append(chfdb[i])
    data_labels.append(chfdb_labels[i])
for i in range(len(ndb)):
    data_features.append(ndb[i])
    data_labels.append(ndb_labels[i])

out=ecg.ecg(signal=chfdb[1][:1024], sampling_rate=125., show=False)

X_train, X_test, y_train, y_test = train_test_split(data_features,data_labels,test_size = 0.30)

clf_2 = DecisionTreeClassifier()
    
    
    #SUBSET 1
clf_2.fit(X_train,y_train)
acc = clf_2.score(X_test,y_test)
pred = clf_2.predict(ndb)

print(acc, pred)
