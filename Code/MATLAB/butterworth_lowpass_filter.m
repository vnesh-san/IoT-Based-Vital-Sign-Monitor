function y = butterworth_lowpass_filter(data,cutoff,fs,order)

[b,a] = butterworth_lowpass(cutoff,fs,order);
y = filter(b, a, data);

end
