from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mn112233@localhost/dbweb?charset=utf8mb4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
except:
    print("ko sql")

db = SQLAlchemy(app=app)
login =LoginManager(app=app)