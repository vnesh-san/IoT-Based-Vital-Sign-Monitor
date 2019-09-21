tic;
ndb_ecg   = load('ecg_dataset_ndb.csv');
chfdb_ecg = load('ecg_dataset_chf.csv'); 
spo2 = load('spo2.csv');
chfdb=[];
ndb=[];
chfdb_sq=[];
ndb_sq=[];
qrs=[]; 
loc=[];

a=spo2(1:3:end);
b=spo2(2:3:end);
c=spo2(3:3:end);
spo2_2=[a;b;c];
spo2_2=spo2_2.';

IR_AC_heart_signal = sum(spo2_2(:,1))/length(spo2_2);
Heart_rpm = sum(spo2_2(:,2))/length(spo2_2);
Oxygen_saturation = sum(spo2_2(:,3))/length(spo2_2);

t = linspace(0,8.192,1024);
i=1;

while(i<=length(chfdb_ecg))
    fil_ecg = chfdb_ecg(i,:); 
    wt = modwt(fil_ecg,5);
    wtrec = zeros(size(wt));
    wtrec(4:5,:) = wt(4:5,:);
    y = imodwt(wtrec,'sym4');
    chfdb = [chfdb; y];
    chfdb_sq = [chfdb_sq; abs(y).^2];
    i=i+1;
end
i=1;
while(i<=length(ndb_ecg))
    fil_ecg = ndb_ecg(i,:); 
    wt = modwt(fil_ecg,5);
    wtrec = zeros(size(wt));
    wtrec(4:5,:) = wt(4:5,:);
    y = imodwt(wtrec,'sym4');
    ndb = [ndb; y];
    ndb_sq = [ndb_sq; abs(y).^2];
    i=i+1;
end
toc/60

csvwrite('chfdb_ecg.csv',chfdb);
csvwrite('chfdb_sq.csv',chfdb_sq);
csvwrite('ndb_ecg.csv',ndb);
csvwrite('ndb_sq.csv',ndb_sq);