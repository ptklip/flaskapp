This is a Python Flask project:

Work on Flask techniques

Perform web scraping, ETL, etc.

How to
------

Start the Flask app in debug mode:

set FLASK_APP=flaskapp
set FLASK_ENV=development
flask run

Run the app interactively:

flask shell

Run in Gunicorn:

pip install gunicorn
gunicorn --workers=2 --bind=0.0.0.0:8000 app:flaskapp


See all environmental variables in Windows:

env

To do:

- Get data from SQL Server and insert into PostgreSQL
   
    Use pyodbc to connect. - Check
        "C:\development\etl\conn_sql_server.py"
        - Trusted connection
        - Create PostgreSQL table to hold the data
        - Insert the rows in PostgreSQL.

- Let logged in users see these ETL jobs and status information.

- Etc.
