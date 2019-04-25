from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ae4a5462339fad4e4924c778ec41cd07'

from flaskblog import routes