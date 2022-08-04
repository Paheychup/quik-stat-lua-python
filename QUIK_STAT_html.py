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
today= (date.today() - timedelta(days=1)).strftime("%Y%m%d") #return prev date
#today='20220615'
#------------------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def f_txtfiles(today):
    txtfiles = []
    for file in glob.glob(".\\lua_output_txt\\*IPADDRESS*"+today+"*.txt"):
            txtfiles.append(file)
    return txtfiles
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
    df=df[df['delta_time']<10]
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
    df=df.sort_values(['Market','type'],ascending=[True,False])
    return df
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#------------------------------------------------------------------------------
df=f_df_transform(df)
#------------------------------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#------------------------------------------------------------------------------
'''fig=px.scatter(data_frame=df,x='date_time',y='seconds',title='QUIK STATISTICS'
               ,color='type')'''
'''
fig=px.scatter(data_frame=df,x='date_time',y='seconds',title='QUIK STATISTICS'
               ,color='Market',hover_name='Market'
               ,hover_data=['order_num','date_time','seconds','type']

               )
fig.update_layout({'xaxis':{'title':{'text':'Date_time'}},
                   'yaxis':{'title':{'text':'Response to transaction in seconds'}}})
#plot(fig)
'''


#------------------------------------------------------------------------------
# визуализируем данные https://plotly.com/python/reference/index/
color_map= {'FR': 'rgb(235, 52, 52)' , 'CETS': 'rgb(235, 149, 52)', 'FORTS': 'rgb(67, 52, 235)'}

fig=px.scatter(data_frame=df,x='date_time',y='seconds',title='QUIK STATISTICS'
            #,facet_col='Market'
            ,symbol='type'
            ,color='Market'
            ,hover_name='Market'
            #,hover_data=['order_num','date_time','seconds','type']
            ,hover_data={'order_num':True,'date_time':True,'seconds':True,'type':True}
            ,color_discrete_map=color_map
            #,symbol_sequence= ['circle', 'circle-open-dot', 'square','square-open-dot','diamond','diamond-open-dot']
            ,symbol_sequence= ['circle','circle-open-dot']
            #,color_discrete_sequence=['blue', 'orange', 'green', 'brown','black','yellow']
               )
fig.update_layout({'title':{'font':{'size':20},'x':0.5,'xanchor':'center'}})
#-----------------------------------------------------------------------------------------------
# drop_down buttons
# Create the buttons
dropdown_buttons = [
    {'label': "ALL MARKETS", 'method': "update", 'args': [{"visible": [True, True,True,True,True,True]}, {"title": "QUIK STATISTIC"}]},
    {'label': "CETS send_order", 'method': "update", 'args': [{"visible": [True, False, False,False,False,False]}, {"title": "CETS send_order"}]},
    {'label': "CETS kill_order", 'method': "update", 'args': [{"visible": [False, True, False, False,False,False]}, {"title": "CETS kill_order"}]},
    {'label': "FORTS send_order", 'method': "update", 'args': [{"visible": [False, False, True,False,False,False]}, {"title": "FORTS send_order"}]},
    {'label': "FORTS kill_order", 'method': "update", 'args': [{"visible": [False, False, False, True, False, False]}, {"title": "FORTS kill_order"}]},
    {'label': "FR send_order", 'method': "update", 'args': [{"visible": [False, False, False,False,True,False]}, {"title": "FR send_order"}]},
    {'label': "FR kill_order", 'method': "update", 'args': [{"visible": [False, False, False, False,False,True]}, {"title": "FR kill_order"}]},
]
# Update the figure to add dropdown menu
fig.update_layout({
  		'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})
#-----------------------------------------------------------------------------------------   
# legend and axis update
# create legend dictionary
my_legend={'title':{'text':'ALL MARKETS','font':{'color':'red'}}
            ,'bgcolor':'rgb(246,228,129)'
            ,'bordercolor':'black','borderwidth':1
            ,'font':{'size':16}
            ,'groupclick':'toggleitem'
            #,'orientation':'h'
            #,'yanchor':'top'
            #,'y':0.99
            #,'xanchor':'right'
            #,'x':0.2
            }

fig.update_layout({ 
                'xaxis':{'title':{'text':'Date_time','font':{'size':20}}}
                ,'yaxis':{'title':{'text':'Response to transaction in seconds','font':{'size':20}}}
                ,'legend':my_legend
                })
#-----------------------------------------------------------------------------------------         
# hover update  
''' # first method
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)
'''
# second method
fig.update_layout({'hoverlabel':{'bgcolor':'white','font_size':16}})
#-----------------------------------------------------------------------------------------         
# marker update  

''' # first method
fig.update_traces(marker=dict(size=10,
                              line=dict(width=1,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
'''
# second method
fig.update_traces({'marker': {'size':10,'line':{'width':1,'color':'DarkSlateGrey'}} } )
#fig.update_traces({'marker': {'size':20,'line':{'width':1,'color':'DarkSlateGrey'}} }, {'selector':{'mode':'markers'}} )
#-----------------------------------------------------------------------------------------  
# add annotation example
'''
annotation = { 
    # set coordinates of annotation
    'xref':'paper', 'yref':'paper', 'x':0.5,'y':1.01
    # set text and format
    ,'bgcolor':'blue'
    ,'showarrow':False
    ,'text':'Server QUIK'
    ,'font':{'color':'white','family':'Courier New','size':14}
    }
'''
#annotation1={'font':{'size':16}}
#annotation2={'font':{'size':16}}
#annotation3={'font':{'size':16}}
#fig.update_layout({'annotations':[annotation]})
#fig.update_layout({'annotations':[annotation1,annotation2,annotation3]})

#-----------------------------------------------------------------------------------------  
# plot data
#plot(fig)

#path=os.getcwd()+'\QUIK_STAT_html'
#plot(figure_or_data=fig,filename=path+'\QUIK_STAT_'+today+'.html',auto_open=False)
#------------------------------------------------------------------------------

path=os.getcwd()+'\QUIK_STAT_html'
plot(figure_or_data=fig,filename=path+'\QUIK_STAT_'+today+'.html',auto_open=False)
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
_=sns.swarmplot(data=df,x='Market',y='seconds')
_=plt.title('QUIK STATISTICS')
_=plt.xlabel('Market')
_=plt.ylabel('transactions time (seconds)')
plt.savefig(path+'\QUIK_STAT_'+today+'.png')











