# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 13:13:10 2021
@author: chupakhin
"""
#%reset -f
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import os
import glob
#import math
from datetime import date, timedelta
#from datetime import datetime
import seaborn as sns
#==============================================================================
print (os.getcwd())
os.chdir('c:\\QUIK_for_stat\\lua')
#------------------------------------------------------------------------------
"""today = date.today()
# YYmmdd
d1 = today.strftime("%Y%m%d")
print("d1 =", d1)"""
#today = date.today().strftime("%Y%m%d")
#prev_day
today= (date.today() - timedelta(days=1)).strftime("%Y%m%d") #return prev date
#today='20220107'
#------------------------------------------------------------------------------
def f_txtfiles(today):
    txtfiles = []
    for file in glob.glob(".\\IPADDRESS*"+today+"*.txt"):
            txtfiles.append(file)
    return txtfiles
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
txtfiles=f_txtfiles(today=today)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_df_append(txtfiles):
    file=0
    if len(txtfiles)!=1:
        while (file<len(txtfiles)):
            try:
                df
            except:
                df=pd.read_csv(txtfiles[file],sep=';',header=0)
                file=+1
                print('except')
            print('next')
            df_temp=pd.read_csv(txtfiles[file],sep=';',header=0)
            df=df.append(df_temp)
            file=+1
    else:
        df=pd.read_csv(txtfiles[file],sep=';',header=0)  
    return df
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
df=f_df_append(txtfiles)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_df_transform(df):
    df=df.reset_index()
    del df['index']
    df[['date','local_time']]=df[['date','local_time']].astype(str)
    df['len_local_time']=df.local_time.map(len)
    df.loc[df['len_local_time']==5,'local_time']='0'+df['local_time']
    df.loc[df['len_local_time']==4,'local_time']='00'+df['local_time']
    df.loc[df['len_local_time']==3,'local_time']='000'+df['local_time']
    df.loc[df['len_local_time']==2,'local_time']='0000'+df['local_time']
    df.loc[df['len_local_time']==1,'local_time']='0000'+df['local_time']
    del df['len_local_time']
    df['date_time']=df['date']+' '+df['local_time']
    df['date_time']=pd.to_datetime(df['date_time'],format='%Y%m%d %H%M%S')
    df=df.set_index('date_time')
    df['date_time']=df.index
    df.index.name=None
    df=df.sort_values(by=['date_time'])
    df['seconds']=df.delta_time
    df=df.drop(['delta_time'],axis=1)
    df['Market']=df.Stock
    df=df.drop(['Stock'],axis=1)
    return df
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
df=f_df_transform(df)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_df_scatterplot(df,today):
    paletter_colors={'send_order':"green",'kill_order':'red'}
    g=sns.relplot(x='date_time',y='seconds',kind='scatter',
                data=df
                ,hue='type'
                #,style='type'
                ,alpha=0.7
                ,size='seconds'
                ,palette=(paletter_colors)
                ,row='Market'
                ,row_order=(['FR','CETS','FORTS','SPB'])
                #,col='type'
                #,col_order=(['send_order','kill_order'])
                #,style=(10,100)
                ,height=2
                #,aspect=11.7/8.27
                ,aspect=5
                )
    #g.fig.suptitle('QUIK STATISTIC',y=1.02) #add title to plot
    #g.set(xlabel='Xlabel',ylabel='Ylabel')
    #plt.xticks(rotation=90) #rotate xticks
    #g.set(ylabel='time (seconds)',yscale='log')
    #g.set(ylabel='seconds')
    #g.set(yscale='log')
    g.savefig('\QUIK_STAT_PNG\QUIK_STAT_'+today+'.png')
    #type_of_g=type(g)
    #print('type_of_g='+str(type_of_g))
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
sns.set_style('whitegrid')
sns.set(rc={"figure.dpi":300, 'savefig.dpi':300})
sns.set_context('paper')

f_df_scatterplot(df=df, today=today)


'''# increase the scale
sns.set_context('paper')
sns.set_context('notebook')
sns.set_context('talk')
sns.set_context('poster')
'''
