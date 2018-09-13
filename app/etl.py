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
from sqlalchemy import create_engine
import psycopg2 
import io
import datetime

DATABASE_URL=os.environ['DATABASE_URL']

def red_sox_batting_stats():
    # Get a page from the web
    url = 'https://www.baseball-reference.com/teams/BOS/2018.shtml'
 
    response = requests.get(url)

    # Process page from the web.
    soup = BeautifulSoup(response.text, 'lxml')

    # Find the batting stats table.
    table = soup.find('table', id='team_batting')

    # Create a matrix:
    # For each row, get the text from each cell.
    # The table has empty cells which must be replaced by something,
    # e.g. 'null', in order to preserve row length.
    outer_list = []
    for row in table.find_all('tr'):
        inner_list = []
        for cell in row.find_all('td'):
            text = cell.text
            inner_list.append(''.join(text) if text else 'null')
        outer_list.append(inner_list)

    # Create a pandas DataFrame from the matrix.   
    df = pd.DataFrame(outer_list)
    df.columns = ['Pos', 'Name', 'Age', 'G', 'PA', 'AB', 'R', 'H', '2B', \
        '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', \
        'OPS+', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB']

    # Drop rows that do not contain stats.
    df = df[~df['Pos'].isin(['null'])]
    df = df.dropna()
    # Replace 'null' with 0. Replace (strings in parentheses) with nothing.
    # Replace '*' with nothing. Replace '#' with nothing.
    df = df.replace('null', 0).replace(r'\(.*\)', '', regex=True) \
        .replace(r'\*', '', regex=True).replace(r'\#', '', regex=True)
    
    # print(df.to_string()) # Print the DataFrame to the screen.

    current_date = datetime.datetime.today().strftime('%Y-%m-%d')

    
    engine = create_engine(DATABASE_URL)
    conn = engine.raw_connection()
    cur = conn.cursor()

    # Truncate the staging table.
    sql = """
    TRUNCATE TABLE batting_stats_current_season_staging
    """

    cur.execute(sql)
    conn.commit()

    # Insert the DataFrame into the PostgreSQL staging table.
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=True)
    output.seek(0)
    cur.copy_from(output, 'batting_stats_current_season_staging')
    conn.commit()

    # TO DO:
    # Check the row count.
    # The row count should be with 75% of previous rowcount.
    # If False, stop and alert.
    # If true, proceed.
    # Log ETL metadata to  database table.

    # Insert into main table with select from staging table.
    sql = """
    INSERT INTO batting_stats_current_season (
        position,
        player_name,
        age,
        games_played,
        plate_appearences,
        at_bats,
        runs_scored,
        hits, doubles,
        triples,
        home_runs,
        runs_batted_in,
        stolen_bases,
        caught_stealing,
        bases_on_balls,
        strike_outs,
        batting_average,
        on_base_percentage,
        slugging_percentage,
        on_base_plus_slugging,
        on_base_percentage_plus,
        total_bases,
        grounded_into_double_play,
        hit_by_pitch,
        sacrifice_hits,
        sacrifice_flies,
        intentional_bases_on_balls,
        insert_date
    )
    SELECT
        position,
        player_name,
        age,
        games_played,
        plate_appearences,
        at_bats,
        runs_scored,
        hits, doubles,
        triples,
        home_runs,
        runs_batted_in,
        stolen_bases,
        caught_stealing,
        bases_on_balls,
        strike_outs,
        batting_average,
        on_base_percentage,
        slugging_percentage,
        on_base_plus_slugging,
        on_base_percentage_plus,
        total_bases,
        grounded_into_double_play,
        hit_by_pitch,
        sacrifice_hits,
        sacrifice_flies,
        intentional_bases_on_balls,
        to_date('{}', 'YYYY-MM-DD')
    FROM batting_stats_current_season_staging
    """.format(current_date)

    cur.execute(sql)
    conn.commit()

    # Truncate staging table.
    sql = """
    TRUNCATE TABLE batting_stats_current_season_staging
    """

    cur.execute(sql)
    conn.commit()

if __name__ == '__main__':
    red_sox_batting_stats()

