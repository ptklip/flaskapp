from flask import Flask
import os

flaskapp = Flask(__name__)

from app import routes

flaskapp.config.update(dict(
    SECRET_KEY=os.environ['SECRET_KEY']
))