# -*- coding: utf-8 -*-

"""Use the records Python library to interact with a PostgreSQL database.
# https://github.com/kennethreitz/records
"""
import os
import records

# Gets environment variable DATABASE_URL from the pipenv .env file
# when the environment is activated with 'pipenv shell' or 'pipenv run'
DATABASE_URL=os.environ['DATABASE_URL']

db = records.Database(DATABASE_URL)
rows = db.query("SELECT * FROM users")

for r in rows:
    print("Name: {}\tThing: {}".format(r.name, r.thing))