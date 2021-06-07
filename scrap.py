import requests
from bs4 import BeautifulSoup
import json


def format(data):
    temp = [raw.strip() for raw in data.strings if raw.strip()
            and "[" not in raw.strip()]
    return temp


def cint(x):
    return x.replace(',', '')


def convert(data):
    try:
        if not ("No data" in data[1] or cint(data[1]).isdigit()):
            return
        return {"country": data[0],
                "cases": cint(data[1]),
                "death": cint(data[2]),
                "recovered": cint(data[3])}
    except Exception:
        return


def scrap_data():
    html_doc = requests.get(
        'https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory').text

    soup = BeautifulSoup(html_doc, 'html.parser')
    tag_info = soup.find("table", {"id": "thetable"}).find(
        'tbody').find_all('tr')[1:]
    # print(tag_info)
    # fdata = format(tag_info[1])
    data = []
    for tr in tag_info:
        ctr = convert(format(tr))
        if ctr:
            data.append(ctr)
    with open("data.json", "w") as f:
        json.dump({"data": data}, f)
    return {"data": data}
