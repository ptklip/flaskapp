# -*- coding: utf-8 -*-
"""
Get Red Sox batting statistics from baseball-reference.com.
Turn it into a pandas DataFrame.
Insert the data into PostgreSQL.

"""
import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import os
import records

DATABASE_URL=os.environ['DATABASE_URL']
db = records.Database(DATABASE_URL)

def red_sox_batting_stats():
    # Get a page from the web
    url = 'https://www.baseball-reference.com/teams/BOS/2018.shtml'
    # Save local copy for testing:
    # url_to_scrape = '2018.shtml'

    response = requests.get(url)
    # print(response.status_code)

    # Process page from the web.
    soup = BeautifulSoup(response.text, 'lxml')

    # Or process local file.
    # with open('2018.shtml', 'r') as f:
    #     soup = BeautifulSoup(f, 'lxml')

    table = soup.find('table', id='team_batting')

    outer_list = []
    for row in table.find_all('tr'):
        inner_list = []
        for cell in row.find_all('td'):
            text = cell.text
            inner_list.append(''.join(text) if text else 'null')
        outer_list.append(inner_list)
        
    df = pd.DataFrame(outer_list)
    df.columns = ['Pos', 'Name', 'Age', 'G', 'PA', 'AB', 'R', 'H', '2B', \
        '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', \
        'OPS+', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB']

    # Drop rows that do not contain stats.
    df = df[~df['Pos'].isin(['null'])]
    df = df.dropna()
    # Replace 'null' with 0.
    df = df.replace('null', 0)

    # TODO: Remove text in parantheses in Name column.
    # Example: (10-day dl)
    # var regExp = /\(([^)]+)\)/;

    print(df.to_string())

    from sqlalchemy import create_engine
    import psycopg2 
    import io

    #engine = create_engine('postgres://flaskapp_user:924462@localhost/flaskapp')
    engine = create_engine(DATABASE_URL)
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=True)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'batting_stats_current_season')
    conn.commit()

if __name__ == '__main__':
    red_sox_batting_stats()

