#!/usr/bin/env python
# coding: utf-8
import json
import chart_studio.plotly as py
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scrap
import requests
API="http://213.188.253.139:8000/"

def save_news():
	news_list=requests.get(API+"/api/news").json()
	with open("news.save","w") as newsfile:
		json.dump(news_list,newsfile)
def save_stats():
	total_stats={"world":dict(),"india":dict()}
	india_stats=requests.get(API+"/api/total").json()
	total_stats['india']={"Total":india_stats['cases'],"Active":india_stats['hospitalized'],"Cured":india_stats['cured'],"Deaths":india_stats['death']}
	world_stats=scrap.scrap_data()['data'][0]
	total_stats['world']={"Total":world_stats['cases'],"Active":world_stats['cases']-(world_stats['death']+world_stats['recovered']),"Cured":world_stats['recovered'],"Deaths":world_stats['death']}
	with open("stats.save","w") as statfile:
		json.dump(total_stats,statfile)
def save_india():
	india_map=requests.get(API+"/india").text
	with open("india.html","w",encoding="utf8") as map:
		map.write(india_map)
def save_world():
	df=pd.read_csv('2014_world_gdp_with_codes.csv')
	df3=pd.DataFrame.from_dict(pd.read_json('data.json'))
	df3=df3['data']
	country=[]
	active=[]
	death=[]
	recover=[]
	text=[]
	for i in df3:
		country.append(i['country'])
		death.append(i['death'])
		recover.append(i['recovered'])
		active.append(i['cases'])
		text.append("Country:"+i['country']+"<br>Active:"+str(i['cases'])+"<br>Recovered:"+str(i['recovered'])+"<br>Deaths:"+str(i['death']))
	df2=pd.DataFrame({'COUNTRY':country,'active':active,'recover':recover,'death':death,'text':text})
	df=pd.merge(df,df2,how='inner',on='COUNTRY')
	fig = go.Figure()
	data=dict(type='choropleth',locations=df['CODE'],z=df['active'],showscale=False,colorscale='redor',
         text=df['text'],marker=dict(line=dict(color='#2d383a',width=1)))
	layout=dict(geo=dict(showocean=True,oceancolor='lightblue', showframe=False, projection={'type':'orthographic'}))
	fig.update_layout(showlegend=False,annotations=[dict(go.layout.Annotation(
                text='Some<br>multi-line<br>text',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.1,
                y=0.8,
                bordercolor='black',
                borderwidth=0
            ))])
	chormap=go.Figure([data],layout)
	chormap.write_html('world.html')
def save_data():
	save_news()
	save_stats()
	save_india()
	save_world()




