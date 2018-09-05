This is a project to learn Flask.

How to
------

Start the Flask app in debug mode:

set FLASK_APP=flaskapp
set FLASK_ENV=development
flask run

See all environmental variables in Windows:

env

To do:

- Add logging

- Add roles

- Get data from SQL Server and insert into PostgreSQL
   
    Use pyodbc to connect. - Check
        "C:\development\etl\conn_sql_server.py"
        - Trusted connection
        - Create PostgreSQL table to hold the data
        - Insert the rows in PostgreSQL.

- Get data from the web and insert into PostgreSQL

- Let logged in users see these ETL jobs and status information.

