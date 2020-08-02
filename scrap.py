import requests
from bs4 import BeautifulSoup
import json

def format(data):
    temp=[ raw.strip() for raw in data.strings if raw.strip() and not "[" in raw.strip() ]
    return temp

def cint(x):
    return x.replace(',','')

def convert(data):
    try:
        return {"country":data[0],
                "cases":int(cint(data[1])),
                "death":int(cint(data[2])),
                "recovered":int(cint(data[3]))}
    except:
        return None


def scrap_data():
    html_doc=requests.get('https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory#covid19-container').text

    soup=BeautifulSoup(html_doc,'html.parser')
    tag_info=soup.find("table", {"id": "thetable"}).find('tbody').find_all('tr')[1:]
    #print(tag_info)
    fdata=format(tag_info[1])
    data=[]
    for tr in tag_info:
        tr = convert(format(tr))
        if tr:
            data.append(tr)
    with open("data.json","w") as f:
        json.dump({"data":data},f)
    return {"data":data}