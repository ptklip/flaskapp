# -*- coding: utf-8 -*-
"""
Flask Application

Move data around in a PostgreSQL database.

"""

from pg import pg_conn
import os
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    # Call pg_conn as a test to see if the DB conn is working.
    # It is. The query result prints to the terminal in debug mode.
    pg_conn()
    return "\nThe Flask app responded ok.\n\n"

@app.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)
    

if __name__ == '__main__':
    app.run()
