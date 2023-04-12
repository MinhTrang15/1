from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from urllib.parse import quote
from flask_login import LoginManager


app = Flask(__name__)


app.secret_key = '#%^&(*$%^&(78678675$%&^&$^%*&^%&*^'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hospital?charset=utf8mb4" % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['THUOC_KEY'] = 'thuoc'


db = SQLAlchemy(app=app)
login = LoginManager(app=app)

