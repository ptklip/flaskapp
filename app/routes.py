# -*- coding: utf-8 -*-

from flask import (
  Flask, g, request, redirect, url_for, render_template, flash, session
)
import os
import records
#https://docs.python.org/3/howto/logging-cookbook.html
import logging
from app import flaskapp
from app.forms import LoginForm, NotesForm # Import each form defined in forms.py.

DATABASE_URL=os.environ['DATABASE_URL']
db = records.Database(DATABASE_URL)

logger = logging.getLogger('flaskapp')
logger.setLevel(logging.DEBUG)
# Create file handler which logs even debug messages
fh = logging.FileHandler('flaskapp.log')
fh.setLevel(logging.DEBUG)
# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    print('session.get("logged_in") = ', session.get('logged_in'))
    return render_template('index.html')

@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # print('username: ', username, 'password: ', password)

        sql =""" 
            SELECT username, user_password 
            FROM users
            WHERE username = $${}$$ AND user_password = crypt('{}', user_password);
            """.format(
            username, password)
        # print(sql)

        row = db.query(sql).first()
        if row is not None:
            # print('User password is correct')
            session['logged_in'] = True
            username = row['username']
            logger.info('A user has logged in: {}'.format(username))
            flash('Welcome, {}. You are logged in.'.format(username))
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@flaskapp.route("/logout")
def logout():
    session['logged_in'] = False
    
    print('session.get("logged_in") = ', session.get('logged_in'))
    flash('You have logged out.')
    return render_template('index.html', form=LoginForm())  

@flaskapp.route('/users')
def users():
    # Login required
    if not session.get('logged_in'):
        flash('Please log in to view that page.')
        return render_template('login.html', form=LoginForm())

    username = 'johndoe'

    # sql = 'SELECT * from users'

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

    rows = db.query(sql)

      
    return render_template('users.html', title='Users', recordset=rows)

@flaskapp.route('/notes', methods=['GET', 'POST'])
def notes():
    form=NotesForm()
    if not session.get('logged_in'):
        flash('Please log in to view that page.')
        return render_template('login.html', form=LoginForm())

    # Let the user enter a new note into the database.
    if request.method == 'POST':
        note = request.form['note']
        #note = 'Test'

        insert_sql ="""
                INSERT INTO notes (note) VALUES ($${}$$)
                """.format(
                note)
        
        print(insert_sql)
        # To Do: Prevent empty insert.
        db.query(insert_sql)

        # Redirect so the user sees an empty form after submitting a note.
        if form.validate_on_submit():
            return redirect(url_for('notes'))

    # Display the existing notes from the database.
    select_sql ="""
            SELECT note FROM notes
            """
    # print(select_sql)

    rows = db.query(select_sql)
    
    return render_template('notes.html', title='Notes', form=NotesForm(), recordset=rows)

@flaskapp.route('/etl')
def etl():
    if not session.get('logged_in'):
        flash('Please log in to view that page.')
        return render_template('login.html', form=LoginForm())
    
    sql ="""
            SELECT job_name, job_description , last_run_time , last_run_status FROM etl_jobs
            """
    rows = db.query(sql)
    return render_template('etl.html', recordset=rows)