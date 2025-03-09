import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Movies & TV Series Tracker", page_icon="🎥", layout="wide")


@st.cache_data  # 👈 Add the caching decorator
def load_data():
    # sqlite3 connection and get/load data
    conn = sqlite3.connect("movies_tv_shows.db")
    
    all_data_df = pd.read_sql_query("SELECT * FROM MAIN_DATA", conn)
    all_episodes_df = pd.read_sql("SELECT * FROM EPISODES", conn)

    # Create filtered DataFrames
    all_movies_df = all_data_df[all_data_df["TYPE"] == "Movie"]
    all_tv_shows_df = all_data_df[all_data_df["TYPE"] == "TV Series"]
    movies_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "Movie") ]
    tv_shows_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "TV Series") ]
    tv_shows_active_df = all_data_df[ (all_data_df["STATUS"] == "IN PROGRESS") & (all_data_df["TYPE"] == "TV Series") ]

    
    
    conn.close()
    
    return all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df


# Defining general variables (Only define the variable if it doesn't exist in session_state)
if "current_year" not in st.session_state:
    st.session_state.current_year = pd.to_datetime('today').year

if "current_month" not in st.session_state:
    st.session_state.current_month = pd.to_datetime('today').month


# ✅ Load data only once & store separately
if (
    "all_data_df" not in st.session_state
    or "all_movies_df" not in st.session_state
    or "all_tv_shows_df" not in st.session_state
    or "movies_watched_df" not in st.session_state
    or "tv_shows_active_df" not in st.session_state
    or "tv_shows_watched_df" not in st.session_state
    or "all_episodes_df" not in st.session_state
):
    
    all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df = load_data()
    
    st.session_state.all_data_df = all_data_df
    st.session_state.all_movies_df = all_movies_df
    st.session_state.all_tv_shows_df = all_tv_shows_df
    st.session_state.movies_watched_df = movies_watched_df
    st.session_state.tv_shows_watched_df = tv_shows_watched_df
    st.session_state.tv_shows_active_df = tv_shows_active_df
    st.session_state.all_episodes_df = all_episodes_df
    #st.experimental_rerun()  # Forces a re-run (It didn't work)
    
    st.success("✅ Data loaded successfully!")





# Navigation
page_home = st.Page("page_home.py", title="Home", icon=":material/house:")
page_movies = st.Page("page_movies.py", title="Movies", icon="🎦", url_path="movies")
page_tv_shows = st.Page("page_tv_shows.py", title="TV Shows", icon="📺", url_path="tv-shows")

pg = st.navigation([page_home, page_movies, page_tv_shows])


pg.run()

