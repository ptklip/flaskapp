#!/usr/bin/python3
'''
Test Flask

'''

from flask import Flask, render_template
from werkzeug.serving import run_simple
import psycopg2 as pg

app = Flask(__name__)

def pg_conn():
    conn = pg.connect("dbname=flaskapp_dev user=peter")

    cur = conn.cursor()
    '''Create a PostgreSQL database connection.'''

    print('\nPostgreSQL database version:')

    sql = "SELECT version()"
    cur.execute(sql)

    # Display the PostgreSQL database server version.
    db_version = cur.fetchone()
    print(db_version)

    # close the connection.
    cur.close()


@app.route("/")
def root():

    txt = pg_conn()    

    return "\nThe Flask app responded ok.\n\n"

@app.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)


if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, app)
