#!/usr/bin/python3
'''
Test Flask

'''

from flask import Flask
app = Flask(__name__)

@app.route("/")
def root():
    return "\nThe Flask app responded ok.\n\n"

@app.route('/<name>')
def greet_named_visitor(name):
    return "\nWelcome, {}\n\n".format(name)

if __name__ == "__main__":
    app.run()
