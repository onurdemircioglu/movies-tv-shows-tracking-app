import streamlit as st
import pandas as pd

st.title("📺 TV Shows")
#st.write("Keep track of your favorite TV series!")

# Access stored DataFrames
if (
    "all_data_df" in st.session_state 
    #and "all_movies_df" in st.session_state 
    #and "movies_watched_df" in st.session_state
    #and "all_tv_shows_df" in st.session_state
    #and "tv_shows_watched_df" in st.session_state
    #and "tv_shows_active_df" in st.session_state
    #and "all_episodes_df" in st.session_state
    and "tv_shows_last_watched_df" in st.session_state
):
    # Last 30 Days Watched
    st.write("Latest TV Shows I am following.")
    #st.image("https://via.placeholder.com/300x200", caption="Example Movie")
    tv_shows_last_watched_df2 = st.session_state.tv_shows_last_watched_df.copy()
    
    # Sorting
    tv_shows_last_watched_df2 = tv_shows_last_watched_df2.sort_values(["MAX_WATCHED_DATE", "TITLE"], ascending=[False, True]) # .reset_index(drop=True)
    
    # Printing
    st.dataframe(tv_shows_last_watched_df2.head(20), hide_index=True, column_order=("ID", "TYPE", "IMDB_TT", "TITLE", "RELEASE_YEAR", "DURATION", "RATING", "RATING_COUNT", "GENRES", "MAX_WATCHED_DATE", "LATEST_EPISODE"))