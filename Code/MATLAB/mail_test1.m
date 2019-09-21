setpref('Internet','SMTP_Server','smtp.gmail.com');
setpref('Internet','E_mail','viku.vignesh96@gmail.com');
setpref('Internet','SMTP_Username','viku.vignesh96@gmail.com');
setpref('Internet','SMTP_Password','krishna@key');
props = java.lang.System.getProperties;
props.setProperty('mail.smtp.auth','true');
props.setProperty('mail.smtp.socketFactory.class', 'javax.net.ssl.SSLSocketFactory');
props.setProperty('mail.smtp.socketFactory.port','465');
sendmail('viku.vignesh96@gmail.com','texttobesent','HI') ;