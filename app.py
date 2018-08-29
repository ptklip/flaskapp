#!/usr/bin/python3
'''
Test Flask

'''

from flask import Flask, render_template
from werkzeug.serving import run_simple
import psycopg2 as pg

app = Flask(__name__)


@app.route("/")
def index():

    conn = pg.connect("dbname=flaskapp user=peter")

    cur = conn.cursor()
    '''Create a PostgreSQL database connection.'''

    output = "\nPostgreSQL database version:\n\n"

    sql = "SELECT version()"
    cur.execute(sql)

    # Display the PostgreSQL database server version.
    db_version = str(cur.fetchone())
    output += db_version

    # close the connection.
    cur.close()    

    end = "\nThe Flask app responded ok.\n\n"
    output += end
    return output

@app.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)


if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, app)


