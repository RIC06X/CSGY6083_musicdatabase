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

@st.cache
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

"## Browse tables"
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





"## Find all songs of an artist "
sql_all_artist = "SELECT DISTINCT(name) FROM artist;"
try:
    artists = query_db(sql_all_artist)["name"].tolist()
    artist = st.selectbox("Choose an artist", artists,1)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if artist:
    f"Display the table"

    sql_all= f"select song.name, song.duration_ms, song.release_date from artist, song_artist_map, song where artist.aid = song_artist_map.aid and song_artist_map.sid = song.sid and artist.name = '{artist}'; "
    try:
        df = query_db(sql_all)
        st.dataframe(df)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")


"## select songs from a playlist given playlist name "
sql_playlist = "select pname from playlist;"
try:
    data_rows = query_db(sql_playlist)["pname"].tolist()
    select_data = st.selectbox("Choose a playlist", data_rows,1)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if select_data:
    f"Display the table"

    sql_all_songs= f"select song.name song_name, album.name album_name, song.duration_ms, song.release_date from playlist, playliststores, song, album where playlist.pid = playliststores.pid and song.sid = playliststores.sid and song.album_id = album.album_id and playlist.pname = '{select_data}' order by song.name;"
    try:
        df = query_db(sql_all_songs)
        st.dataframe(df)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")


"## Let the user search for an artist and the system can display the song and the album information corresponding to the searched artist"
artist_searched = st.text_input('Type the artist name here:')

if artist_searched:
    f"Display the result"
    sql_find_information = f"""
        SELECT artist.name artist_name, song.name song_name, album.name album_name
        FROM artist, song, album, album_artist_map aam, song_artist_map sam
        WHERE artist.name LIKE '{artist_searched}%'
        AND artist.aid = aam.aid
        AND album.album_id = aam.album_id
        AND song.sid = sam.sid
        AND artist.aid = sam. aid;
    """
    try:
        test1 = query_db(sql_find_information)
        st.dataframe(test1)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

"## Find all artists that belongs to a certain company and show his/her songs count"
sql_all_company = "select company.name from company;"
try:
    data_rows = query_db(sql_all_company)["name"].tolist()
    select_data = st.selectbox("Choose a company", data_rows,1)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if select_data:
    f"Display the table"

    sql_all_info= f"""
        select company.name company_name, artist.name artist_name, count(*) song_total
        from company, artistowned, artist, song_artist_map
        where artistowned.aid = artist.aid
        and company.company_id = artistowned.company_id
        and song_artist_map.aid = artist.aid
        and company.name = '{select_data}'
        group by company.name, artist.name;
    """
    try:
        df = query_db(sql_all_info)
        st.dataframe(df)
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")

"## Find songs that has duration < N seconds from a playlist"
sql_playlist = "select pname from playlist;"
select_duration = 500
try:
    data_rows = query_db(sql_playlist)["pname"].tolist()
    select_data = st.selectbox("Choose a playlist", data_rows)
    select_duration  = st.slider('duration (second)', value=[0, 1000], step=10)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if select_data:
    f"Display the table"

    sql_all_info= f"""
        select song.name song_name, album.name album_name, song.duration_ms, song.release_date
        from playlist, playliststores, song, album
        where playlist.pid = playliststores.pid
        and song.sid = playliststores.sid
        and song.album_id = album.album_id
        and playlist.pname = '{select_data}'
        and duration_ms < '{select_duration[1] * 1000}'
        and duration_ms > '{select_duration[0] * 1000}';
    """
    try:
        df = query_db(sql_all_info)
        st.dataframe(df.to_dict())
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")


# "## Leave a review"
# st.subheader("Leave a review please")
# conduct_every_song= 'SELECT name FROM song;'

# choose_song= st.selectbox('Please choose a song', conduct_every_song)
# rating=st.selectbox('Rating',[1,2,3,4,5])
# if st.button("Submit"):
#     update_rating(rating,choose_song)
#     st.success("Thank you for leaving a rating")
    

