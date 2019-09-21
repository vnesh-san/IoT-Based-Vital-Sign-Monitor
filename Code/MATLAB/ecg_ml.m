chfdb = load ('chfdb_ecg.csv');
ndb   = load ('ndb_ecg.csv');
ecg   = load ('ecg.csv');

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






