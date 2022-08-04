# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 10:31:57 2022

@author: Chupakhin Paul

execute commad in python script example
"""
import os
from datetime import date, timedelta

#print (os.getcwd())
os.chdir('c:\\QUIK_for_stat\\lua\\python')

#------------------------------------------------------------------------------
"""today = date.today()
# YYmmdd
d1 = today.strftime("%Y%m%d")
print("d1 =", d1)"""
#today = date.today().strftime("%Y%m%d")
#prev_day
prev_date= (date.today() - timedelta(days=1)).strftime("%Y%m%d") #return prev date
#today='20220126'
#------------------------------------------------------------------------------
#filename='QUIK_STAT_'+prev_date+'.html'
#filename='c:\QUIK_for_stat\lua\QUIK_STAT_Reports\QUIK_STAT_'+prev_date+'.html'
#filename='..\QUIK_STAT_'+prev_date+'.html'
filename='..\QUIK_STAT_html\QUIK_STAT_'+prev_date+'.html'
filename2='..\QUIK_STAT_html\QUIK_STAT_'+prev_date+'.png'
recipients='quikadmin@open.ru,shumova@open.ru'
#recipients='chupakhin@open.ru'
#servInfo_name='servInfo_'+prev_date+'.txt'
#os.system( "ipconfig /all > ipconfig_all.txt"  )
cmd_command='Postie.exe -esmtp -host:relayopen.open-broker.ru -to:'+recipients+'\
     -from:support@open.ru -user:quick_dsp_mail\
         -pass:ichiajoD0theeghiezeeHoh2ieNgokah -s:"Quik statistics scatterplot"\
             -a:'+filename+' -msg:QuikStat scatter'
''''cmd_command='Postie.exe -esmtp -host:relayopen.open-broker.ru -to:quikadmin@open.ru;shumova@open.ru\
     -from:support@open.ru -user:quick_dsp_mail\
         -pass:ichiajoD0theeghiezeeHoh2ieNgokah -s:"Quik statistics"\
             -a:'+filename+' <'+servInfo_name+' ' '''
#print(cmd_command)
os.system( cmd_command )
cmd_command2='Postie.exe -esmtp -host:relayopen.open-broker.ru -to:'+recipients+'\
     -from:support@open.ru -user:quick_dsp_mail\
         -pass:ichiajoD0theeghiezeeHoh2ieNgokah -s:"Quik statistics swarmplot"\
             -a:'+filename2+' -msg:QuikStat swarmplot'
os.system( cmd_command2 )