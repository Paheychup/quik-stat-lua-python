# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:43:03 2022

@author: chupakhin paul
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 13:13:10 2021
@author: chupakhin paul
"""
#%reset -f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
#import math
from datetime import date, timedelta
#from datetime import datetime
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

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
today = (date.today() - timedelta(days=0)).strftime("%Y%m%d") #return prev date
#today='20220411'
path=os.getcwd()+'\QUIK_STAT_html'

#temp
server='ДСП'
#server='Айтеко'
server='q1.open-broker.ru_sd'
server='q3.open-broker.ru_s'
server='q3.open-broker.ru_sd'
server='q2.open-broker.ru_s'
server='q2.open-broker.ru_as'
#server='q2.open-broker.ru'
#server='q1.open-broker.ru'
#server='q3.open-broker.ru'
#uid='231875'
#server='vserv'
#------------------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_txtfiles(today):
    txtfiles = []
    for file in glob.glob(".\\lua_output_txt\\ITERATIONS*"+server+"*_"+today+"*.txt"):
            txtfiles.append(file)
    return txtfiles
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''def f_txtfiles(today):
    txtfiles = []
    for file in glob.glob(".\\lua_output_txt\\ITERATIONS*"+server+"*_"+uid+"*_"+today+"*.txt"):
            txtfiles.append(file)
    return txtfiles'''
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#------------------------------------------------------------------------------
txtfiles=f_txtfiles(today=today)
#------------------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_df_append(txtfiles):
    file=0
    if len(txtfiles)>1:
        while (file<len(txtfiles)):
            try:
                df
            except:
                df=pd.read_csv(txtfiles[file],sep=';',header=0)
                file=+1
                #print('except file='+str(file))
  
            #print('next')
            df_temp=pd.read_csv(txtfiles[file],sep=';',header=0)
            df=df.append(df_temp)
            file=file+1
            #print('file='+str(file))
    elif len(txtfiles)==1:
        df=pd.read_csv(txtfiles[file],sep=';',header=0)  
    return df
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#------------------------------------------------------------------------------
df=f_df_append(txtfiles)
#------------------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_df_transform(df):
    df=df.reset_index()
    del df['index']
    #df=df[df['delta_time']<10]
    df[['date','local_time']]=df[['date','local_time']].astype(str)
    df['len_local_time']=df.local_time.map(len)
    df.loc[df['len_local_time']==5,'local_time']='0'+df['local_time']
    df.loc[df['len_local_time']==4,'local_time']='00'+df['local_time']
    df.loc[df['len_local_time']==3,'local_time']='000'+df['local_time']
    df.loc[df['len_local_time']==2,'local_time']='0000'+df['local_time']
    df.loc[df['len_local_time']==1,'local_time']='00000'+df['local_time']
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
#------------------------------------------------------------------------------
df=f_df_transform(df)
#------------------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_stat(df):
    market_list=df.Market.unique()
    for i in market_list:
        stat=df[df.Market==i]
        print(i)
        print(stat.describe().seconds)
    return stat.describe().seconds
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
stat=f_stat(df)
stat[0:]=round(stat[0:],6)
stat[0:][:]
stat[:][:].to_csv(path+'\QUIK_STAT_ITERATIONS_'+server+'_'+today+'.txt',sep=':',header=False)
#------------------------------------------------------------------------------

p = sns.stripplot(x="Market", y="seconds", data=df, size=4
                  ,dodge=True
                  )
#plt.xticks(rotation=45, ha="right")
# plot the mean line
sns.boxplot(showmeans=True,
            meanline=True,
            #meanprops={'color': 'purple', 'ls': '-', 'lw': 2},
            meanprops={'linestyle': '-.','lw': 1,'color':'brown'},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            zorder=2,
            x="Market",
            y="seconds",
            data=df,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=p)
plt.ylabel('transactions time (seconds)')
plt.title('QUIK STATISTICS  '+server+'  '+today)
#plt.text(x=0.51,y=0.08,s="An annotation")
'''
plt.text(
         x=0.31
        ,y=round(stat[1],3)+round(stat[1],3)/100*10
        ,s=(str(stat.index[0])+": "+str(round(stat[0],0))+"\n"+
         str(stat.index[1])+": "+str(round(stat[1],3))+"\n"+
         str(stat.index[3])+": "+str(round(stat[3],3))+"\n"+
         str(stat.index[7])+": "+str(round(stat[7],3)))
        )
'''
plt.savefig( path+'\QUIK_STAT_ITERATIONS_'+server+'_'+today+'.png',dpi=100)
#plt.savefig( path+'\QUIK_STAT_ITERATIONS_UID_231875_'+server+'_'+today+'.png',dpi=100)






#------------------------------------------------------------------------------
#work
fig=px.box(df,color='Market',y='seconds'
           ,x='Market', points='all'
           #,hover_name=('Market')
           ,hover_data=['order_num','date_time','seconds']
           ,title='QUIK STATISTICS '+server+' '+today
           )
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="left",
    x=0.0,title=''))
fig.update_layout({'xaxis':{'title':{'text':'Market'}},
                   'yaxis':{'title':{'text':'Response to transaction in seconds'}}})
plot(figure_or_data=fig,filename=path+'\QUIK_STAT_ITERATIONS_'+server+'_'+today+'.html',auto_open=False)
#------------------------------------------------------------------------------




















#------------------------------------------------------------------------------
'''fig=px.scatter(data_frame=df,x='date_time',y='seconds',title='QUIK STATISTICS'
               ,color='type')'''
fig=px.scatter(data_frame=df,x='date_time',y='seconds',title='QUIK STATISTICS'
               ,color='Market',hover_name='Market'
               ,hover_data=['order_num','date_time','seconds','type']

               )
fig.update_layout({'xaxis':{'title':{'text':'Date_time'}},
                   'yaxis':{'title':{'text':'Response to transaction in seconds'}}})
#plot(fig)
path=os.getcwd()+'\QUIK_STAT_html'
plot(figure_or_data=fig,filename=path+'\QUIK_STAT_ITERATIONS_'+today+'.html',auto_open=False)
#plot(figure_or_data=fig,filename=path+'\QUIK_STAT_'+today+'.html',auto_open=False)
#------------------------------------------------------------------------------
sns.set()
'''
sns.set_context('paper')
_=sns.catplot(data=df,x='Market',y='seconds',kind='swarm',hue='type'
              ,alpha=0.8)
_=plt.title('QUIK STATISTICS')
_=plt.xlabel('Market')
_=plt.ylabel('transactions time (seconds)')
plt.savefig(path+'\QUIK_STAT_'+today+'.png')
'''
_=sns.swarmplot(data=df,x='Market',y='seconds',dodge=True)

_=plt.title('QUIK STATISTICS  '+server+'  '+today)
_=plt.xlabel('Market')
_=plt.ylabel('transactions time (seconds)')
plt.savefig(path+'\QUIK_STAT_ITERATIONS_'+today+'.png')
#------------------------------------------------------------------------------

p = sns.stripplot(x="Market", y="seconds", data=df, size=4
                  ,dodge=True
                  )
#plt.xticks(rotation=45, ha="right")
# plot the mean line
sns.boxplot(showmeans=True,
            meanline=True,
            #meanprops={'color': 'purple', 'ls': '-', 'lw': 2},
            meanprops={'linestyle': '-.','lw': 1,'color':'brown'},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            zorder=2,
            x="Market",
            y="seconds",
            data=df,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=p)
plt.ylabel('transactions time (seconds)')
plt.title('QUIK STATISTICS  '+server+'  '+today)
plt.savefig( path+'\QUIK_STAT_ITERATIONS_'+server+'_'+today+'.png',dpi=100)
#------------------------------------------------------------------------------
#work
fig=px.box(df,color='Market',y='seconds'
           ,x='Market', points='all'
           #,hover_name=('Market')
           ,hover_data=['order_num','date_time','seconds']
           ,title='QUIK STATISTICS '+server+' '+today
           )
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="left",
    x=0.0,title=''))
fig.update_layout({'xaxis':{'title':{'text':'Market'}},
                   'yaxis':{'title':{'text':'Response to transaction in seconds'}}})
plot(fig)
plot(figure_or_data=fig,filename=path+'\QUIK_STAT_ITERATIONS_'+server+'_'+today+'.html',auto_open=False)



#------------------------------------------------------------------------------
fig=px.violin(df,y='seconds',x='Market',color='type',box=True,points='all'
              ,hover_data=['order_num','date_time','seconds']
              ,title='QUIK transaction time '+server
              ,color_discrete_sequence=["green","red"]
              
              )
fig.update_layout({'xaxis':{'title':{'text':'Market'}},
                   'yaxis':{'title':{'text':'Response to transaction in seconds'}}})
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01,
    title="Order type"
))
plot(fig)
plot(figure_or_data=fig,filename=path+'\QUIK_STAT_ITERATIONS_'+server+'_'+today+'.html',auto_open=False)

#------------------------------------------------------------------------------
fig=px.box(df, y='seconds',x='Market',points='all'
              ,hover_data=['order_num','date_time','seconds']
              ,title='QUIK transaction time '+server
              )
fig.update_layout({'xaxis':{'title':{'text':'Market'}},
                   'yaxis':{'title':{'text':'Response to transaction in seconds'}}})
fig.update_traces(marker_color='#3D9970')
#fig.update_layout(title_text="Box Plot Styling Outliers")
plot(fig)
#------------------------------------------------------------------------------

fig=go.Figure()
fig.add_trace(go.Box(
    y=df[df.Market=='CETS'].seconds.values
    ,name='CETS'
    ,boxpoints='all'
    ,marker_color='#3D9970'
    ,line_color='#3D9970'
    ,jitter=0.3,
    pointpos=-1.8
    ))
fig.add_trace(go.Box(
    y=df[df.Market=='FORTS'].seconds.values
    ,name='FORTS'
    ,boxpoints='all'
    ,marker_color='#FF4136'
    ,line_color='#FF4136'
    ,jitter=0.3,
    pointpos=-1.8
    ))
fig.add_trace(go.Box(
    y=df[df.Market=='FR'].seconds.values
    ,name='FR'
    ,boxpoints='all'
    ,marker_color='#FF851B'
    ,line_color='#FF851B'
    ,jitter=0.3,
    pointpos=-1.8
    ))
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="left",
    x=0.0
))
fig.update_layout(
    title='Points Scored by the Top 9 Scoring NBA Players in 2012',
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    #showlegend=False
)
plot(fig)
plot(figure_or_data=fig,filename=path+'\QUIK_STAT_ITERATIONS_'+today+'.html',auto_open=False)
#------------------------------------------------------------------------------
fig=px.box(df,y='seconds',x='Market',color='type',points='all'
              ,hover_data=['order_num','date_time','seconds'])
plot(fig)
#------------------------------------------------------------------------------
fig=px.strip(df,x='Market',y='seconds')
plot(fig)
#------------------------------------------------------------------------------
fig=px.strip(df,color='Market',y='seconds',x='type')
plot(fig)
#------------------------------------------------------------------------------
fig=px.box(df,color='Market',y='seconds',x='type',log_y=True,points='all')
plot(fig)
#------------------------------------------------------------------------------
'''
fig=px.box(data_frame=df,y='seconds'
           ,hover_name='type',hover_data=['Market','order_num','seconds'])
plot(figure_or_data=fig)

#------------------------------------------------------------------------------
fighist=px.histogram(data_frame=df,x='seconds',nbins=10,log_y=True)
fig.update_layout
plot(figure_or_data=fighist)
#------------------------------------------------------------------------------
'''







