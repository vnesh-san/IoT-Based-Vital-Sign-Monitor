
figure
plot(t,chfdb_sq)
title('R-Waves Localized by Wavelet Transform')
hold on
plot(locs,qrspeaks,'ro')
xlabel('Seconds')
title('R Peaks Localized by Wavelet Transform with Automatic Annotations')
heart_rate = length(locs)*60/t(end);

figure
plot(t,fil_ecg,'k--')
hold on
plot(t,y,'r','linewidth',1.5)
set(gca,'xlim',[10.2 12])
legend('Raw Data','Wavelet Reconstruction', ...
    'Location','SouthEast');
xlabel('Seconds')