# -*- coding: utf-8 -*-
"""
pg.py

PostgreSQL database functions.

"""
import os
import records
import psycopg2 as pg

# def pg_conn():
#     # Gets environment variable DATABASE_URL from the pipenv .env file
#     # when the environment is activated with 'pipenv shell' or 'pipenv run'
#     DATABASE_URL=os.environ['DATABASE_URL']

#     db = records.Database(DATABASE_URL)
#     rows = db.query("SELECT username, email FROM users")

#     for r in rows:
#         print("username: {}".format(r.username))


def pg_conn():
    # Gets environment variable DATABASE_URL from the pipenv .env file
    # when the environment is activated with 'pipenv shell' or 'pipenv run'
    DATABASE_URL=os.environ['DATABASE_URL']

    db = records.Database(DATABASE_URL)
    return db

def pg_query(db, sql):
    db = db
    sql = sql
    recordset = db.query(sql)
    return recordset



    # for r in rows:
    #     print("username: {}".format(r.username))


# "SELECT username, email FROM users"