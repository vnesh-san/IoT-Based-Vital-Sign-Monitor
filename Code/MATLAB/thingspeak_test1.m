o2_sat_diag = 1;
h_rpm_diag = 0;
temp_diag = 1;
ecg_diag = 0;

response = thingSpeakWrite(447659,{o2_sat_diag,h_rpm_diag,temp_diag,ecg_diag},'WriteKey','8NRFAUIWXQYN5EYP','Timeout',20);