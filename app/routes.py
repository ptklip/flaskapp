from flask import render_template
from app import flaskapp

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return render_template('index.html')

@flaskapp.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)