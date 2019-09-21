ecg=0;
spo2=0;
resp=0;
yin=1;
yang=1;
yu=1;
i=0;
j=0;
k=0;
flag=0; % flag==1 ecg recorded flag==2 spo2 recorded

s = serial('com9');
set(s,'BaudRate',9600);   

try
    fopen(s);
catch err
    fclose(instrfind);
    error('Make sure you select the correct COM Port where the Arduino is connected.');
end
Tmax=60; % time for running app
Ts=2e-06;
%figure,
%grid on,
%ax1=subplot(3,1,1);
%ax2=subplot(3,1,2);
%ax3=subplot(3,1,3);

tic
while toc<=Tmax
    k=k+1;
    
    out =strsplit(fgetl(s));
    data(k) =str2num(cell2mat(out(1)));
    pause(0.001);
    
    if (data(k)==1001 | flag==1) & i<=8
        flag=1;
        if(i>=1 & i<5)
            ecg(yin)=data(k);
            yin=yin+1;
        end
        if(i>=5)
            resp(yang)=data(k);
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
    
    if (data(k)==1101 | flag==2) & j<=3
        flag=2;
        if (j>=1)
            spo2(yu)=data(k);
            yu=yu+1;
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
    
       % plot(ax1,t(1:length(ecg)),ecg)
       % plot(ax2,t(1:length(resp)),resp)
       % plot(ax3,t(1:length(spo2)),spo2)
        %drawnow   
end
fclose(instrfind)
