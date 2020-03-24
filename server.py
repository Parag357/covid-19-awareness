from flask import Flask , request, render_template
import json
#from create_db import *
# import sqlite3
# from sqlite3 import Error
import re
import requests
import string
from datetime import datetime
import pickle

app = Flask(__name__)
# PASSWORD="5tr0ng_P@ssW0rD"
PASSWORD="SpeedXXX"

@app.route('/')
def index():
	return render_template('index.html')

app.run(debug=True)