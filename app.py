#!/usr/bin/python3
"""
Test Flask

"""

import logging
import sys

import psycopg2 as pg
from flask import Flask

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)

def pg_conn(sql_in):
    """Create a PostgreSQL database connection."""
    print("sql_in = " + sql_in)
    sql = sql_in
    # Use environment variables here.
    conn = pg.connect("dbname=flaskapp user=peter")
    #print("conn = " + str(conn))
    cur = conn.cursor()
    #print("cur = " + str(cur)
    #cur.execute(sql)
    cur.execute(sql)

    return cur

@app.route("/")
def index():
    return "\nThe Flask app responded ?.\n\n"

@app.route('/<name>')
def hello_name(name):
    #return "\nWelcome, {}.\n\n".format(name)
    n = name
    sql = "select * from users where name = '" + n + "'"
    #sql = "select * from users where name = 'Penny'"
    #sql = "select * from users"
    print(sql)
    cur = pg_conn(sql)
    row_count = 0
    for row in cur:
        row_count += 1
        print("row: %s    %s\n" % (row_count, row))
    
    return "ok"

if __name__ == '__main__':
    app.run()
