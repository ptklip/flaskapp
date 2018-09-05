# -*- coding: utf-8 -*-

from flask import (
  Flask, render_template, request, flash, redirect, url_for, session
)
from app import flaskapp
import os
import records
from app.forms import LoginForm, NotesForm # Be sure to import each form you define in forms.py.

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return render_template('index.html')

@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    DATABASE_URL=os.environ['DATABASE_URL']
    db = records.Database(DATABASE_URL)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print('method is POST')
        print('username: ', username, 'password: ', password)

        sql =   """ 
            SELECT username, user_password 
            FROM users
            WHERE username = $${}$$ AND user_password = crypt('{}', user_password);
            """.format(
            username, password)
            
        print(sql)

        row = db.query(sql).first()
        if row is not None:
            print('yes')

            session['logged_in'] = True
            return redirect(url_for('users'))
        else:
            error = "Wrong username or password."

        

    #     return redirect(next or url_for('index'))
    return render_template('login.html', form=form)
    # return 'ok'
    

@flaskapp.route('/users')
#@login_required
def users():
    ###
    ### Should I use psycopg2 instead of Python records? records has almost no documentation.
    ###
    DATABASE_URL=os.environ['DATABASE_URL']
    db = records.Database(DATABASE_URL)
    username = 'johndoe'

    # sql =   """ 
    #         SELECT username, first_name, last_name, email, phone, user_status, start_time 
    #         FROM users
    #         WHERE username = '{}'
    #         """.format(
    #         username)

    sql =   """ 
            SELECT username, first_name, last_name, email, phone, user_status, DATE(start_time) 
            FROM users
            """

    # sql = 'SELECT * from users'

    # How do I handle it if there are no records?
    rows = db.query(sql)
    
    # print('SQL:')
    # print(sql)
    
    # for r in rows:
    #     colnames = r.keys()
    
    return render_template('users.html', title='Users', recordset=rows)


## Make a page that lets me enter data in a simple table.
@flaskapp.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NotesForm()

    DATABASE_URL=os.environ['DATABASE_URL']
    db = records.Database(DATABASE_URL)

    # Let the user enter a new note into the database.
    if request.method == 'POST':
        note = request.form['note']
        #note = 'Test'

        # $$: Dollar quoting:
        # https://www.postgresql.org/docs/current/static/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING
        # Allows single quotes in an insert.
        ### Make sure no SQL injection, though.
        insert_sql ="""
                INSERT INTO notes (note) VALUES ($${}$$)
                """.format(
                note)
        
        print(insert_sql)
        #print(json.dumps(insert_sql))

        ### Prevent 'None' from being entered into the database. The user needs to add input before submitting.
        db.query(insert_sql)

        # Redirect so the user see an empty form after submitting a note.
        if form.validate_on_submit():
            return redirect(url_for('notes'))

    # Display the existing notes from the database.
    select_sql ="""
            SELECT note FROM notes
            """
    print(select_sql)

    rows = db.query(select_sql)
    # db.close()

    # for r in rows:
    #     colnames = r.keys()
    #     values = r.values()
    #     print(colnames, values)
    
    return render_template('notes.html', title='Notes', form=form, recordset=rows)