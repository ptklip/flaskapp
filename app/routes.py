# -*- coding: utf-8 -*-

from flask import (
  Flask, render_template, request, flash, redirect, url_for, session
)
#from flask import Flask, render_template, request
from app import flaskapp
import os
import records
from app.forms import LoginForm, NotesForm # Be sure to import each form you define in forms.py.

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return render_template('index.html')

@flaskapp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@flaskapp.route('/users')
def users():
    ###
    ### Should I use psycopg2 instead of Python records? records has almost no documentation.
    ###
    DATABASE_URL=os.environ['DATABASE_URL']
    db = records.Database(DATABASE_URL)
    username = 'johndoe'

    sql =   """ 
            SELECT username, first_name, last_name, email, phone, user_status, start_time 
            FROM users
            WHERE username = '{}'
            """.format(
            username)

    # How do I handle it if there are no records?
    rows = db.query(sql, (username))

    print(sql)

    for r in rows:
        colnames = r.keys()
    
    return render_template('users.html', recordset=rows, colnames=colnames)


## Make a page that lets me enter data in a simple table.
@flaskapp.route('/notes', methods=["GET", "POST"])
def notes():
    form = NotesForm()

    

    DATABASE_URL=os.environ['DATABASE_URL']
    db = records.Database(DATABASE_URL)

    if request.method == 'POST':
        note = request.form['note']
        #note = 'Test'

        insert_sql ="""
                INSERT INTO notes (note) VALUES ('{}')
                """.format(
                note)
        print(insert_sql)

        ### Prevent 'None' from being entered into the database. The user needs to add input before submitting.
        db.query(insert_sql)

        # Redirect so the user see an empty form after submitting a note.
        if form.validate_on_submit():
            return redirect(url_for('notes'))

    select_sql ="""
            SELECT note AS Notes FROM notes
            """

    rows = db.query(select_sql)

    for r in rows:
        colnames = r.keys()
    
    return render_template('notes.html', title='Notes', form=form, recordset=rows, colnames=colnames)