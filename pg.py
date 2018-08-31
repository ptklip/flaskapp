# -*- coding: utf-8 -*-
"""
pg.py

PostgreSQL database functions.

"""
import os
import records
import psycopg2 as pg

def pg_conn():
    # Gets environment variable DATABASE_URL from the pipenv .env file
    # when the environment is activated with 'pipenv shell' or 'pipenv run'
    DATABASE_URL=os.environ['DATABASE_URL']

    db = records.Database(DATABASE_URL)
    rows = db.query("SELECT username, thing FROM users")

    for r in rows:
        print("Username: {}\tThing: {}".format(r.username, r.thing))

    # return 1



