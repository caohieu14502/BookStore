#where our web app live
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "super secret key"

app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/booktest?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8
app.config['COMMENT_SIZE'] = 10

db = SQLAlchemy(app=app)

cloudinary.config(
        cloud_name='ddivten1j',
        api_key='498755371621665',
        api_secret='5BvKEWbX8ZyDjCBob-doHeZxDj4')


login = LoginManager(app=app)