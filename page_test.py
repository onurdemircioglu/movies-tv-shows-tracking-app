import sys
sys.path.append(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app")

import streamlit as st
import pandas as pd
import sqlite3

import my_functions

st.title("Update Record")

db_path = (r"C:\Users\onur\anaconda3\envs\movies_streamlit\app\movies_tv_shows.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

df = pd.read_sql_query(
    """SELECT ID, IMDB_TT, TYPE,
    --, TITLE_TYPE,
    ORIGINAL_TITLE, PRIMARY_TITLE,
    RELEASE_YEAR, 
    STATUS, SCORE, SCORE_DATE,
    GENRES, DURATION, RATING, RATING_COUNT,
    WATCH_GRADE, BEYAZPERDE_LINK
    FROM MAIN_DATA WHERE 1=1""", conn)
original_df = df.copy()         


imdb_link = st.text_input("IMDb Link", value="https://www.imdb.com/title/", key="imdb_link")
find_record_button = st.button("Find Record", key="find_record")

# Initialize edited_df in session state if it doesn't exist
if "edited_df" not in st.session_state:
    st.session_state.edited_df = pd.DataFrame()


if find_record_button:
    imdb_link = st.session_state.get("imdb_link", "")
    obj = my_functions.MyClass()
    
    # Convert imdb link to tt format
    if "/title/tt" in imdb_link:
        imdb_in = obj.imdb_converter(imdb_link, "in")
        edited_df = st.data_editor(df[df["IMDB_TT"]==imdb_in], num_rows="fixed", disabled=("ID", "IMDB_TT"), key="edited_data", hide_index=True)


if not st.session_state.edited_df.empty: #only display the data editor if the edited_df is not empty.
    edited_df = st.data_editor(st.session_state.edited_df, num_rows="fixed", disabled=("ID", "IMDB_TT"), key="edited_data", hide_index=True)

    if st.button("Update Database"):
        original_df['ORIGINAL_TITLE'] = original_df['ORIGINAL_TITLE'].str.strip()
        edited_df['ORIGINAL_TITLE'] = edited_df['ORIGINAL_TITLE'].str.strip()
        original_df['GENRES'] = original_df['GENRES'].str.strip()
        edited_df['GENRES'] = edited_df['GENRES'].str.strip()

        # Force ID columns to be integers
        original_df['ID'] = original_df['ID'].astype(int)
        edited_df['ID'] = edited_df['ID'].astype(int)

        if not original_df.equals(edited_df):
            updates = False
            for index, row in edited_df.iterrows():
                record_id = row['ID']
                st.write(f"Record ID from edited_df: {record_id}") #added for debugging
                original_row = original_df.loc[original_df['ID'] == record_id]

                if not original_row.equals(pd.DataFrame([row], columns=edited_df.columns)):
                    new_original_title = row['ORIGINAL_TITLE']
                    new_genre = row['GENRES']
                    new_rating = row['RATING']

                    st.write(f"Updating record {record_id} - Original Title: {new_original_title}, Genres: {new_genre}, Rating: {new_rating}")

                    try:
                        cursor.execute(
                            "UPDATE MAIN_DATA SET ORIGINAL_TITLE = ?, GENRES = ?, RATING = ? WHERE ID = ?",
                            (new_original_title, new_genre, new_rating, record_id)
                        )
                        updates = True
                        st.write(f"SQL update executed for ID: {record_id}")
                    except sqlite3.Error as e:
                        st.error(f"Database update error: {e}")

            if updates:
                try:
                    conn.commit()
                    st.success("✅ Database updated successfully!")
                    st.write("Database Commited")
                except sqlite3.Error as e:
                    st.error(f"Database commit error: {e}")
            else:
                st.warning("No changes detected!")
        else:
            st.warning("No changes detected!")

conn.close()





