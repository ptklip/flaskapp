#!/usr/bin/python3
'''
Test Flask

'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result


print(os.environ['APP_SETTINGS'])

@app.route("/")
def root():
    return "\nThe Flask app responded ok.\n\n"

@app.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}\n\n".format(name)

if __name__ == "__main__":
    app.run()
