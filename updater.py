#!/usr/bin/env python
# coding: utf-8
import json
import pandas as pd
import plotly.graph_objs as go
import requests
API = "http://covid-awareness-api.herokuapp.com"


def save_news():
    response = requests.get(API+"/news").json()
    with open("news.save", "w") as newsfile:
        json.dump({"news": response}, newsfile)


def save_world():
    df = pd.DataFrame.from_dict(json.load(open('world_codes.json'))['data'])
    response = requests.get(API+"/stats").json()
    df3 = pd.DataFrame.from_dict(response)
    df3['text'] = ("Country:"+df3['country']+"<br>Active:"+df3['cases'] +
                   "<br>Recovered:"+df3['recovered'] +
                   "<br>Deaths:"+df3['death'])
    df = pd.merge(df, df3, how='inner', on='country')
    data = dict(
        type='choropleth',
        locations=df['code'],
        z=df['cases'],
        showscale=False,
        colorscale='redor',
        text=df['text'],
        marker=dict(line=dict(color='#2d383a', width=1)))
    layout = dict(geo=dict(showocean=True, oceancolor='lightblue',
                           showframe=False,
                           projection={'type': 'orthographic'}))
    chormap = go.Figure([data], layout)
    chormap.write_html('world.html')


def save_data():
    save_news()
    save_world()
