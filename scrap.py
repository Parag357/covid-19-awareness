import requests
from bs4 import BeautifulSoup
import json

def format(data):
	temp=[ raw.strip() for raw in data.strings if raw.strip() ]
	if '[' in temp[1]:
		del temp[1]
	return temp
def cint(x):
	try:
		return int(x.replace(',',''))
	except:
		return 0
def scrap_data():
	html_doc=requests.get('https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory#covid19-container').text

	soup=BeautifulSoup(html_doc,'lxml')
	tag_info=soup.find_all('tbody')[1]
	tag_info=tag_info.find_all('tr')
	fdata=format(tag_info[1])
	data_dict=dict()
	data_dict["country"]="World"
	data_dict["cases"]=cint(fdata[1])
	data_dict["death"]=cint(fdata[2])
	data_dict["recovered"]=cint(fdata[3])
	data=[data_dict]
	for k in range(2,len(tag_info)-2):
		temp=format(tag_info[k])
		data_dict=dict()
		data_dict["country"]=temp[0]
		data_dict["cases"]=cint(temp[1])
		data_dict["death"]=cint(temp[2])
		data_dict["recovered"]=cint(temp[3])
		data.append(data_dict)
	# print(data)
	with open("data.json","w") as f:
		json.dump({"data":data},f)
	return {"data":data}