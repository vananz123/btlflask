from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
app = Flask(__name__)
app.secret_key = '$%^*&())(*&%^%4678675446&#%$%^&&*^$&%&*^&^'
app.config['USER_KEY'] = 'user'
cloudinary.config(cloud_name='dg3ozy1rg',
                  api_key='279553511589541',
                  api_secret='6u93kMrTz4RRZrAYfphJ1dwMIoE')
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mn112233@localhost/dbweb?charset=utf8mb4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
except:
    print("ko sql")

db = SQLAlchemy(app=app)
login =LoginManager(app=app)