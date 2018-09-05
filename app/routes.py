# -*- coding: utf-8 -*-

from flask import (
  Flask, g, request, redirect, url_for, render_template, flash, session
)
import os
import records
from app import flaskapp
from app.forms import LoginForm, NotesForm # Import each form defined in forms.py.

DATABASE_URL=os.environ['DATABASE_URL']
db = records.Database(DATABASE_URL)

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    """Logic for the index page."""
    print('session.get("logged_in") = ', session.get('logged_in'))
    return render_template('index.html')

@flaskapp.route('/login', methods=['GET', 'POST'])
def login():
    """Logic for the login page."""
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
            flash('Welcome. You are logged in.')
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
    """Logic for the notes page."""
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