from flask import Flask , request, render_template, Markup
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os

app = Flask(__name__,template_folder=".",static_folder='assets')

@app.route('/')
def index():
	URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&authuser=0'	
	cd = datetime.now().day
	cm = datetime.now().month
	response = requests.get(URL.format(query="Corona india", month=cm, from_day=cd, to_day=cd, year=20)).text
	filtered=response.split('<div class="kCrYT">')[1:]
	news_list=[]
	for x in range(0,len(filtered),2):
		link=(filtered[x][filtered[x].find("https://"):filtered[x].find("&amp;")])
		title=(filtered[x].split('</div>')[0].split('<div')[1].split('>')[1])
		time=filtered[x+1][filtered[x+1].find('<span class="r0bn4c rQMQod">')+28:filtered[x+1].find('</span>')]
		news_list.append({"title":title,"link":link,"time":time})
	news_format="""
	    <div class="row">
      <div class="col-sm-2" align="right">
        <span class="badge badge-dark badge-pill">{time}</span>
      </div>
      <div class="col-sm-10">
        <div class="card44 ">
		<a href="{link}" alt="Link To Article">{title}</a> 
        </div>
      </div>
    </div>"""
	news_html="\n\n".join([news_format.format(title=news["title"],link=news["link"],time=news["time"]) for news in news_list ])
	html_doc=requests.get('https://www.worldometers.info/coronavirus/').text
	soup=BeautifulSoup(html_doc,'html.parser')
	out=[]
	ind_stats=[]
	for trtag in soup.find_all('tr'):
		inp=[]
		for tdtag in trtag.find_all('td'):
			inp.append(tdtag.text.strip())
		if 'India' in inp:
			ind_stats=inp
		out.append('|'.join(inp))
	t_case=out[-1].split('|')
	# print(t_case)
	t_case=[t_case[1],t_case[2],t_case[6],t_case[5],t_case[3]]
	ind_stats=[ind_stats[1],ind_stats[2],ind_stats[6],ind_stats[5],ind_stats[3]]
	print(ind_stats)
	hlist=["Total","New","Active","Cured","Deaths"]
	w_html='\n'.join([ '<h3 class="display-5" style="font-family: Righteous, cursive;">'+hlist[i]+' : '+t_case[i]+' </h3>' for i in range(5)])
	i_html='\n'.join([ '<h3 class="display-5" style="font-family: Righteous, cursive;">'+hlist[i]+' : '+ind_stats[i]+' </h3>' for i in range(5)])
	
	return render_template('index.html',news_article=Markup(news_html),world_stats=Markup(w_html),india_stats=Markup(i_html))

@app.errorhandler(404) 
def not_found(e): 
	return render_template('404.html')
port = int(os.environ.get('PORT', 33507))
app.run(port=port,debug=True)