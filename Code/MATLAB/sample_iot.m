o2_sat_diag = 0;
h_rpm_diag = 1;
temp_diag = 1;
ecg_diag = 1;

channelID = 447659;
writeKey  = '8NRFAUIWXQYN5EYP';

thingSpeakWrite(channelID,{o2_sat_diag,h_rpm_diag,temp_diag,ecg_diag},'WriteKey',writeKey)