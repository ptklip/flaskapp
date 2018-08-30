# -*- coding: utf-8 -*-
"""
Flask Application

Move data in and out of a PostgreSQL database.

"""

import os
import records
#import psycopg2 as pg
from flask import Flask


app = Flask(__name__)

def pg_conn():
    # Gets environment variable DATABASE_URL from the pipenv .env file
    # when the environment is activated with 'pipenv shell' or 'pipenv run'
    DATABASE_URL=os.environ['DATABASE_URL']

    db = records.Database(DATABASE_URL)
    rows = db.query("SELECT * FROM users")

    for r in rows:
        print("Name: {}\tThing: {}".format(r.name, r.thing))


@app.route("/")
def index():
    return "\nThe Flask app responded ok.\n\n"

@app.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)
    

if __name__ == '__main__':
    app.run()
