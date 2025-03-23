import streamlit as st
st.set_page_config(page_title="Movies & TV Series Tracker", page_icon="🎥", layout="wide") # ✅ Must be first! or error occurs: set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.

import sys
sys.path.append(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app")

import pandas as pd
import sqlite3
import login  # Import the login system
#login.check_login()


# # Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠️ Please log in first.")
    login.check_login()  # Call the login function only if the user is not logged in
    st.stop()  # Stop further execution until the user logs in
else:
    st.session_state["logged_in"] = True  # Keep logged-in state



#st.write(f"👋 Welcome, {st.session_state['username']}!")
st.write(f"👋 Welcome, {st.session_state.get('username', 'Guest')}!")

# Admin Panel Button (Accessible only by Admins)
if st.session_state.get("role") == "admin":
    if st.button("Go to Admin Panel"):
        st.switch_page("admin_page.py")

# Logout Button
if st.button("Logout"):
    st.session_state.clear()  # Clear session
    st.rerun()  # Refresh the page to show login again


@st.cache_data  # 👈 Add the caching decorator
def load_data():
    # sqlite3 connection and get/load data
    conn = sqlite3.connect(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app\movies_tv_shows.db")
    
    all_data_df = pd.read_sql_query("SELECT * FROM MAIN_DATA", conn)
    all_episodes_df = pd.read_sql("SELECT * FROM EPISODES", conn)
    tv_shows_last_watched_df = pd.read_sql("SELECT * FROM TV_SHOWS_LAST_WATCHED", conn)
    

    # Create filtered DataFrames
    all_movies_df = all_data_df[all_data_df["TYPE"] == "Movie"]
    all_tv_shows_df = all_data_df[all_data_df["TYPE"] == "TV Series"]
    movies_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "Movie") ]
    tv_shows_watched_df = all_data_df[ (all_data_df["STATUS"] == "WATCHED") & (all_data_df["TYPE"] == "TV Series") ]
    tv_shows_active_df = all_data_df[ (all_data_df["STATUS"] == "IN PROGRESS") & (all_data_df["TYPE"] == "TV Series") ]
       
    conn.close()
    
    return all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df, tv_shows_last_watched_df


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
    or "tv_shows_last_watched_df" not in st.session_state
):
    
    all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, tv_shows_watched_df, tv_shows_active_df, all_episodes_df, tv_shows_last_watched_df = load_data()
    
    st.session_state.all_data_df = all_data_df
    st.session_state.all_movies_df = all_movies_df
    st.session_state.all_tv_shows_df = all_tv_shows_df
    st.session_state.movies_watched_df = movies_watched_df
    st.session_state.tv_shows_watched_df = tv_shows_watched_df
    st.session_state.tv_shows_active_df = tv_shows_active_df
    st.session_state.all_episodes_df = all_episodes_df
    st.session_state.tv_shows_last_watched_df = tv_shows_last_watched_df
    #st.experimental_rerun()  # Forces a re-run (It didn't work)
    
    st.success("✅ Data loaded successfully!")


# Navigation
page_home = st.Page("page_home.py", title="Home", icon=":material/house:", url_path="home-page")
page_movies = st.Page("page_movies.py", title="Movies", icon="🎦", url_path="movies-page")
page_tv_shows = st.Page("page_tv_shows.py", title="TV Shows", icon="📺", url_path="tv-shows-page")
page_data_entry = st.Page("page_data_entry.py", title="Data Entry", url_path="data-entry-page")
page_admin = st.Page("admin_page.py", title="Admin Page", url_path="admin-page")
page_test = st.Page("page_test.py", title="Test Page", url_path="test-page")
page_test2 = st.Page("page_test2.py", title="Test Page 2", url_path="page-test2")
page_temp = st.Page("page_temp.py", title="Temp Page", url_path="temp-page")
page_search = st.Page("page_search.py", title="Search", url_path="search-page")


pg = st.navigation([page_home, page_movies, page_tv_shows, page_data_entry, page_admin, page_test, page_test2, page_temp, page_search])


pg.run()















