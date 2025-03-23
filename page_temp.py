import streamlit as st
import sqlite3
import pandas as pd


conn = sqlite3.connect("movies_tv_shows.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM MAIN_DATA ORDER BY ID DESC LIMIT 10")
sql_query = "SELECT * FROM MAIN_DATA ORDER BY ID DESC LIMIT 10"
#last_entries = cursor.fetchall()
last_entries = pd.read_sql_query(sql_query, conn)
cursor = conn.cursor()
conn.close()

st.dataframe(last_entries, hide_index=True)
st.rerun()