#where our web app live
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/booktest?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

cloudinary.config(
        cloud_name='ddivten1j',
        api_key='498755371621665',
        api_secret='5BvKEWbX8ZyDjCBob-doHeZxDj4')
