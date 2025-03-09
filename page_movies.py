import streamlit as st

st.title("🎦 Movies")

st.markdown("#### Keep track of your favorite movies and shows!")

# Access stored DataFrames
if (
    "all_data_df" in st.session_state 
    and "all_movies_df" in st.session_state 
    and "movies_watched_df" in st.session_state
    #and "all_tv_shows_df" in st.session_state
    #and "tv_shows_watched_df" in st.session_state
    #and "tv_shows_active_df" in st.session_state
    #and "all_episodes_df" in st.session_state
):
    # Last 30 Days Watched
    movies_watched_last_30_days_df = st.session_state.movies_watched_df.copy()
    movies_watched_last_30_days_df = movies_watched_last_30_days_df.sort_values(["SCORE_DATE", "ORIGINAL_TITLE"], ascending=[False, True]) # last_30_days_watched_df.sort_values(by="SCORE_DATE", ascending=False)
    movies_watched_last_30_days_df = movies_watched_last_30_days_df.head(20)

    # Favorite Movies (High Rankings)
    movies_high_scored_df = st.session_state.movies_watched_df.copy()
    movies_high_scored_df = movies_high_scored_df[movies_high_scored_df["SCORE"] >= 70].sort_values(["SCORE", "SCORE_DATE", "ORIGINAL_TITLE"], ascending=[False, False, True])

    # Plan to watch (based on watch grade)
    plan_to_watch_df = st.session_state.all_movies_df.copy()
    plan_to_watch_df = plan_to_watch_df[plan_to_watch_df["STATUS"] == "TO BE WATCHED"].sort_values(["WATCH_GRADE", "RATING"], ascending=[False, False])
    plan_to_watch_df = plan_to_watch_df.head(20)


tab1, tab2, tab3 = st.tabs(["📅 Upcoming", "✅ Watched", "⭐ Favorites"])

with tab1:
    st.write("Movies I plan to watch.")
    #st.image("https://via.placeholder.com/300x200", caption="Example Movie")
    st.dataframe(plan_to_watch_df)

with tab2:
    st.write("Last Watched 20 Movies")
    #st.image("https://via.placeholder.com/300x200", caption="Example Watched Movie")
    st.dataframe(movies_watched_last_30_days_df)

with tab3:
    st.write("My favorite movies.")
    #st.image("https://via.placeholder.com/300x200", caption="Example Favorite Movie")
    st.dataframe(movies_high_scored_df)









