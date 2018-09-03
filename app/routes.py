from flask import Flask, render_template
from app import flaskapp
import os
import records

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return render_template('index.html')

@flaskapp.route('/users')
def users():
    DATABASE_URL=os.environ['DATABASE_URL']
    db = records.Database(DATABASE_URL)
    sql = """SELECT username, first_name, last_name, email, phone, user_status, start_time 
            FROM users"""
    rows = db.query(sql)

    for r in rows:
        colnames = r.keys()
    return render_template('users.html', recordset=rows, colnames=colnames)

@flaskapp.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)