#!/usr/bin/env python
# coding: utf-8
import json
import pandas as pd
import plotly.graph_objs as go
import scrap
import requests


def save_news():
    URL = "https://www.google.com/search?hl=en&tbm=nws&as_q={query}"
    response = requests.get(URL.format(query="Corona India")).text
    filtered = response.split('<div class="kCrYT">')[1:-1]
    data = []
    for x in range(0, len(filtered)-1, 2):
        link = filtered[x][filtered[x].find(
            "https://"):filtered[x].find("&amp;")]
        title = filtered[x].split('</div>')[0].split('<div')[1].split('>')[1]
        time = filtered[x+1].split('class="r0bn4c rQMQod">')[1].split("<")[0]
        data.append({"title": title, "link": link, "time": time})
    with open("news.save", "w") as newsfile:
        json.dump({"news": data}, newsfile)


def save_world():
    df = pd.DataFrame.from_dict(json.load(open('world_codes.json'))['data'])
    df3 = pd.DataFrame.from_dict(json.load(open('data.json'))['data'])
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
    scrap.scrap_data()
    save_news()
    save_world()
