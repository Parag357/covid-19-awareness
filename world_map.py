#!/usr/bin/env python
# coding: utf-8

# In[13]:


import chart_studio.plotly as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)
import numpy as np
import pandas as pd
import plotly.graph_objs as go


# In[9]:


df=pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')


# In[10]:


df3=pd.DataFrame.from_dict(pd.read_json('E:/covid-19-awareness/data.json'))
df3=df3['data']
country=[]
active=[]
death=[]
recover=[]
for i in df3:
    country.append(i['country'])
    death.append(i['death'])
    recover.append(i['recovered'])
    active.append(i['cases'])
df2=pd.DataFrame({'COUNTRY':country,'active':active,'recover':recover,'death':death})


# In[11]:


df=pd.merge(df,df2,how='inner',on='COUNTRY')


# In[ ]:





# In[14]:


fig = go.Figure()
data=dict(type='choropleth',locations=df['CODE'],z=df['active'],
         text=df['active'],colorbar={'title':'Country wise case distribution'})
layout=dict(title='covid  19 outbreak',geo=dict(showframe=False, projection={'type':'natural earth'}))
chormap=go.Figure([data],layout)
iplot(chormap)
chormap.write_html('E:/covid-19-awareness/map.html')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




