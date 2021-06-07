from flask import Flask, render_template, Markup
from datetime import datetime
import os
import json
import pickle
import updater
app = Flask(__name__, template_folder=".", static_folder='assets')


@app.route('/')
def index():
    update = False
    now = datetime.now()
    if not os.path.exists('update.save'):
        update = True
    else:
        prev = pickle.load(open('update.save', 'rb'))
        duration = (now-prev).total_seconds()
        duration = divmod(duration, 3600)[0]
        update = duration >= 6
    if update:
        updater.save_data()
        with open('update.save', 'wb') as update_file:
            pickle.dump(now, update_file)
    news_list = json.load(open("news.save", "r"))['news']
    news_format = """
        <div class="row">
      <div class="col-sm-2" align="right">
        <span class="badge badge-dark badge-pill">{time}</span>
      </div>
      <div class="col-sm-10">
        <div class="card44 ">
        <a href="{link}" alt="Link To Article" target="_blank">{title}</a>
        </div>
      </div>
    </div>"""
    news_html = "\n\n".join([news_format.format(
        title=news["title"],
        link=news["link"],
        time=news["time"]) for news in news_list])
    return render_template('index.html', news_article=Markup(news_html))


@app.route('/world')
def world():
    return render_template('world.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port, debug=True)
