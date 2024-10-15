from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from .utils import mkpath

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = (f'sqlite:///{mkpath('data/myapp.db')}')
app.config['SECRET_KEY'] = "cfb1fb6e-c506-413c-9c04-a15124febc96"

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
