from flask import Flask , request, render_template, Markup
import requests
from datetime import datetime

app = Flask(__name__)

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
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span class="badge badge-dark badge-pill">
            <ul class="list-group">
              <li>{time}</li>
            </ul>
          </span>
		  <a href="{link}" alt="Link To Article">
          <div class="container">
              {title}
              </div>
		   </a>
        </li>"""
	news_html="\n\n".join([news_format.format(title=news["title"],link=news["link"],time=news["time"]) for news in news_list ])
	return render_template('index.html',news_article=Markup(news_html))

@app.errorhandler(404) 
def not_found(e): 
	return render_template('404.html')
app.run(debug=True)