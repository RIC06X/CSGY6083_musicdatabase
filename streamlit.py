import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

from dateutil.relativedelta import relativedelta
@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}
def query_db(sql: str):
 
    db_info = get_config()
    # Connect to an existing database
    conn = psycopg2.connect(**db_info)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    # the result is stored in the cursor, function 'execute' returns null
    cur.execute(sql)
    # Obtain data
    data = cur.fetchall() # can use fetchone() or fetchmany(size) instead
    column_names = [desc[0] for desc in cur.description]
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)
    return df

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:
    f"Display the table"

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

"## Query 1: Find all songs of an artist "

sql_all_songs = "SELECT DISTINCT(name) FROM artist ;"
try:
    artists = query_db(sql_all_songs)["name"].tolist()
    artist = st.selectbox("Choose an artist", artists,1)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if artist:
	f"Display the result"

	sql_all_ = sql_order = f"""
    SELECT artist.name, song.name
    FROM artist a, song s, song_artist_map sa
    WHERE a.name = '{artist}' 
    AND a.aid = sa.aid
    AND s.sid = sa.sid
    GROUP BY artist.name; 

    """

	try:
		songs = query_db(sql_all_songs)
		st.dataframe(songs)
	except:
		st.write("Sorry! Something went wrong with your query, please try again.")
