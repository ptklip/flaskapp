import psycopg2 as pg

# The following connection paramters, just dbname and user, work when
# PostgreSQL acess is set to 'trust' for local connections.
conn = pg.connect("dbname=flaskapp_dev user=peter")

cur = conn.cursor()

# Execute a statement
print('\nPostgreSQL database version:')

sql = "SELECT version()"
cur.execute(sql)

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

# close the communication with the PostgreSQL
cur.close()

