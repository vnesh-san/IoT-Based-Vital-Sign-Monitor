ecg=0;
spo2=0;
resp=0;
yin=1;
yang=1;
yu=1;
boo=1;
i=0;
j=0;
k=1;
flag=0; % flag==1 ecg recorded flag==2 spo2 recorded

%ECG : header-1001  footer-1010
%SpO2: header-1101  footer-1110

data=0;
s = serial('com3');
set(s,'BaudRate',9600);   

try
    fopen(s);
catch err
    fclose(instrfind);
    error('Select the correct COM Port where the Arduino is connected.');
end
Tmax=150; % time for running app
Ts=0.008;

tic
while toc<=Tmax   
    
    out =strsplit(fgetl(s));
    data(k) =str2double(cell2mat(out(1)));
    data(isnan(data))=-1;
    
    pause(0.001);
    
    if (data(k)==1001 | flag==1 & data(k)~=-1) & i<=8
        flag=1;
        if(i>=1 & i<5)
            ecg(yin)=(data(k)/1024)*3.3;
            yin=yin+1;
        end
        if(i>=5)
            resp(yang)=(data(k)/1024)*3.3;
            yang=yang+1;
        end
        if i==8
            i=0;
            flag=0;
        else
            i=i+1;
        end
        j=0;
    end
    
    if (data(k)==1101 | flag==2 & data(k)~=-1) & j<=4
        flag=2;
        if (j>=1 & j<=3)
            spo2(yu)=data(k);
            yu=yu+1;
        end
        if (j==4)
            temp(boo)=data(k);
            boo=boo+1;
        end
        j=j+1;
        i=0;
    end
    
    t(k) = toc;
    if k > 1
        T = toc - t(k-1);
        while T < Ts
            T = toc - t(k-1)  ;
        end
    end
    t(k) = toc;
    k=k+1;
    
    
end
fclose(instrfind)


%Filtered signal
fs=500;
cutoff=150;
order=5;
fil_ecg=[];

fil_ecg = butterworth_lowpass_filter(ecg,cutoff,fs,order);
fil_ecg_2=[];
x=1;
a=1;
while (a<=int16(fix(length(ecg)/1024)))
    a=a+1;
    fil_ecg_2=[fil_ecg_2;fil_ecg(x:x+1023)];
    x=x+1023;
end
ecg=[];
ecg_sq=[];
i=1;
len=size(fil_ecg_2);
while(i<=len(1))
    f_ecg = fil_ecg_2(i,:); 
    wt = modwt(f_ecg,5); 
    wtrec = zeros(size(wt));
    wtrec(4:5,:) = wt(4:5,:);
    y = imodwt(wtrec,'sym4');
    ecg = [ecg; y];
    ecg_sq = [ecg_sq; abs(y).^2];
    i=i+1;
end

a=spo2(1:3:end);
b=spo2(2:3:end);
c=spo2(3:3:end);

spo2_2=[a;b;c];
spo2_2=spo2_2.';
IR_AC_heart_signal = sum(spo2_2(:,1))/length(spo2_2);
Heart_rpm = sum(spo2_2(:,2))/length(spo2_2);
O2_sat = sum(spo2_2(:,3))/length(spo2_2);

Temp = sum(temp)/length(temp);

if (O2_sat > 91)
    o2_sat_diag = 0;
else
    o2_sat_diag = 1;
end

if (Heart_rpm > 60 && Heart_rpm < 90)
    h_rpm_diag = 0;
else
    h_rpm_diag = 1;
end

if (Temp >=36.5 & Temp<=38)
    temp_diag = 0;
else
    temp_diag = 1;
end

chfdb = load ('chfdb_ecg.csv');
ndb   = load ('ndb_ecg.csv');

chf_size = size(chfdb); 
ndb_size = size(ndb);
chfdb_label = zeros(chf_size(1),1);
ndb_label = ones(ndb_size(1),1);
features = [chfdb ; ndb];
labels   = [chfdb_label ; ndb_label];
dataset=[features labels];

p = .7  ;    % proportion of rows to select for training
N = size(dataset,1);  % total number of rows 
tf = false(N,1);    % create logical index vector
tf(1:round(p*N)) = true;     
tf = tf(randperm(N));   % randomise order
dataTraining = dataset(tf,:); 
dataTesting = dataset(~tf,:); 

XT = dataTraining(:,1:end-1);
yT = dataTraining(:,end);
Xt = dataTesting(:,1:end-1);
yt = dataTesting(:,end);

Mdl = fitctree(XT,yT);
L = loss(Mdl,Xt,yt);

pred = predict(Mdl,ecg);

i=1;
c0 = 0;
c1 = 0;
while(i<length(pred))
    if (pred(i) == 1)
        c1 = c1+1;
    else
        c0 = c0+1;
    end
    i = i+1;
end

if (c1>c0)
    ecg_diag = 0;
else
    ecg_diag = 1;
end

channelID = 447659;
writeKey  = '8NRFAUIWXQYN5EYP';

thingSpeakWrite(channelID,{O2_sat,Heart _rpm,Temp,ecg_diag},'WriteKey',writeKey)

csvwrite('ecg.csv',ecg);
csvwrite('ecg_sq.csv',ecg_sq);
csvwrite('resp.csv',resp.');
csvwrite('spo2.csv',spo2_2);