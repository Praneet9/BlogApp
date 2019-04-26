from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ae4a5462339fad4e4924c778ec41cd07'
bcrypt = Bcrypt(app)

from flaskblog import routes