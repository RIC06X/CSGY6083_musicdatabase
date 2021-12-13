# CSGY6083 MusicDB
by Yanjie Xu and Hanqing Zhang

## Framework 
*Streamlit*

## Language
- Postgresql
- python

## Installation
create table

`cd CSGY6083_musicdatabase`

`psql -d {DatabaseName} -a -f code/schema.sql`

Insert values

`cd data`

`bash load_csv.sh`

Run Streamlit 

`cd ../code`

`streamlit run project.py`

## Data source
- Spotify API

## Last Update
2021-12-12

 
