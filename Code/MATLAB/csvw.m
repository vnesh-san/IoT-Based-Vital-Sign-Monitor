csvwrite('chfdb_ecg.csv',chfdb);
csvwrite('chfdb_sq.csv',chfdb_sq);
csvwrite('ndb_ecg.csv',ndb*10);
csvwrite('ndb_sq.csv',ndb_sq*1e04);