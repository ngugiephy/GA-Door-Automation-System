# Authored by Donatus - https://github.com/Donatussss/imageapp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dt import FlaskDt, get_class_by_tablename
# login modules
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imageapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
dt = FlaskDt(app, db, "display.html", "tables")

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
app.config['SECRET_KEY'] = '6a49u18e4731ba013c5c037c'

bcrypt = Bcrypt(app)

from myimageapp import routes