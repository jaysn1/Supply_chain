from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = '176dea20ac76bb0034290da307893266'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(application)
application.config['UPLOAD_FOLDER'] = os.getcwd() + '/flasksite/data'

from flasksite import routes