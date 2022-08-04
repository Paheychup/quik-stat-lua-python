# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 13:13:10 2021
@author: chupakhin
"""
#==============================================================================
import smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

#print (os.getcwd())
os.chdir('c:\\QUIK_for_stat\\lua')

days_to_subtract=1  
prev_date = (date.today() - timedelta(days=days_to_subtract)).strftime("%Y%m%d")

sender_email = "support@open.ru"
receiver_email = ['quikadmin@open.ru','chupakhin@open.ru','Shumova@OPEN.RU']

smtpObj = smtplib.SMTP()
smtpObj.connect('relayopen.open-broker.ru', 25)
smtpObj.login('quick_dsp_mail', 'ichiajoD0theeghiezeeHoh2ieNgokah')
#smtpObj.ehlo()

msg = MIMEMultipart()
msg['Subject'] = 'QUIK STATISTICS'
msg['From'] = sender_email
msg['To'] = ", ".join(receiver_email)

#msgText = MIMEText('<b>%s</b>' % (body), 'html')
#body='Test msg'
#msgText = MIMEText('%s' % (body), 'html')
#msg.attach(msgText)

'''#attach file example
filename = "filename.txt"
msg.attach(MIMEText(open(filename).read()))
'''
with open('QUIK_STAT_' + prev_date +'.png', 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='QUIK_STAT_'+prev_date+'.png')
        msg.attach(img)

smtpObj.sendmail(sender_email,receiver_email,msg.as_string())
smtpObj.quit()

#==============================================================================












