import sys
sys.path.append(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app")

import streamlit as st
import pandas as pd
import sqlite3
import my_functions

db_path = r"movies_tv_shows.db"

st.title("Update Record Last Try")


# UI Components
imdb_link = st.text_input("IMDb Link", value="https://www.imdb.com/title/", key="imdb_link")
find_record_button = st.button("Find Record", key="find_record")


# Function to fetch data
def fetch_record(imdb_link):
    obj = my_functions.MyClass()
    imdb_in = obj.imdb_converter(imdb_link, "in")

    conn = sqlite3.connect(db_path)
    original_df = pd.read_sql_query(
        """SELECT ID, IMDB_TT, TYPE,
        ORIGINAL_TITLE, PRIMARY_TITLE,
        RELEASE_YEAR, 
        STATUS, SCORE, SCORE_DATE,
        DURATION, RATING, RATING_COUNT, GENRES,
        WATCH_GRADE, BEYAZPERDE_LINK
        FROM MAIN_DATA WHERE IMDB_TT = ?""", conn, params=(imdb_in,))
    conn.close()

    # Store in session_state
    st.session_state["original_df"] = original_df if not original_df.empty else None


if find_record_button and "/title/tt" in imdb_link:
    fetch_record(imdb_link)


# Display data only if found
if "original_df" in st.session_state and st.session_state["original_df"] is not None:
    df = st.session_state["original_df"]

    title_type_options = {
        "Movie": ["Movie", "Short", "TV Movie", "TV Special", "Video", "Unknown"],
        "TV Series": ["TV Series", "TV Mini Series", "Unknown"],
        "Unknown": ["Unknown"]
        }
    title_type_options_keys = list(title_type_options.keys())
    title_type_options_keys.append("Select a value")
    title_type_options_keys.insert(0,"Select a value")

    status_options = ["Select a value", "POTENTIAL", "TO BE WATCHED", "MAYBE", "N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"]
    
    with st.container():
        col_original, col_new = st.columns(2)
        
        id_original = df.iloc[0, 0] if not df.empty else ""
        col_original.text_input("Original ID", value=id_original, disabled=True, key="id_original")
        col_new.text_input("New ID", value=id_original, disabled=True, key="id_new",)

        imdb_tt_original = df.iloc[0, 1] if not df.empty else ""
        col_original.text_input("Original IMDb TT", value=imdb_tt_original, disabled=True, key="imdb_tt_original")
        col_new.text_input("New IMDb TT", key="imdb_tt_new")

        type_original = df.iloc[0, 2] if not df.empty else ""
        col_original.text_input("Original Type", value=type_original, disabled=True, key="type_original")
        #col_new.text_input("New Type", value="", key="type_new")

        col_new.selectbox(
          "New Type",
          title_type_options_keys,
          #("1","2","3"),
          index=0,  # Default: "Unknown"
          key="record_type"
          )

        original_title_original = df.iloc[0, 3] if not df.empty else ""
        col_original.text_input("Original Title", value=original_title_original, disabled=True, key="original_title_original")
        col_new.text_input("New Original Title", value="", key="original_title_new")

        primary_title_original = df.iloc[0, 4] if not df.empty else ""
        col_original.text_input("Primary Title", value=primary_title_original, disabled=True, key="primary_title_original")
        col_new.text_input("New Primary Title", value="", key="primary_title_new")

        release_year_original = df.iloc[0,5] if not df.empty else ""
        col_original.text_input("Release Year", value=release_year_original, disabled=True,key="release_year_original")
        col_new.number_input("New Release Year", value=None, min_value=1888, max_value=st.session_state.current_year, key="release_year_new")

        status_original = df.iloc[0,6] if not df.empty else ""
        col_original.text_input("Status", value=status_original, disabled=True,key="status_original")
        col_new.selectbox(
          "New Status",
          status_options,
          #horizontal=True,  # Makes options appear inline
          index=0,  # Default: "POTENTIAL"
          key="status_new"
          )
        
        score_original = df.iloc[0,7] if not df.empty else ""
        col_original.text_input("Score", value=score_original, disabled=True,key="score_original")
        col_new.number_input("New Score", min_value=5, max_value=100, value=5, step=5, key="score_new") # It is define as text_input because when it is number_input min_valus is automatically 0 or 0.00

        score_date_original = df.iloc[0,8] if not df.empty else ""
        col_original.text_input("Score Date", value=score_date_original, disabled=True, key="score_date_original")
        col_new.date_input("New Score Date", value=st.session_state.current_day)

        duration_original = df.iloc[0,9] if not df.empty else ""
        col_original.text_input("Duration", value=duration_original, disabled=True, key="duration_original")
        col_new.number_input("New Duration", min_value=0, value=0, key="duration_new")

        imdb_rating_original = df.iloc[0,10] if not df.empty else ""
        col_original.text_input("IMDb Rating", value=imdb_rating_original, disabled=True, key="imdb_rating_original")
        col_new.number_input("New IMDb Rating", min_value=0.0, max_value=10.0, step=0.10, format="%.1f", key="imdb_rating_new")

        imdb_rating_count_original = df.iloc[0,11] if not df.empty else ""
        col_original.text_input("IMDb Rating Count", value=imdb_rating_count_original, disabled=True, key="imdb_rating_count_original")
        col_new.number_input("New IMDb Rating", min_value=0, value=0, key="imdb_rating_count_new")

        genres_original = df.iloc[0,12] if not df.empty else ""
        col_original.text_input("Genres", value=genres_original, disabled=True, key="genres_original")
        col_new.multiselect(
               'Select a value',
               ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show", "History",
               "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"], key="genres_new")

        watch_grade_original = df.iloc[0,13] if not df.empty else ""
        col_original.text_input("Watch Grade", value=watch_grade_original, disabled=True, key="watch_grade_original")
        col_new.number_input("New Watch Grade", min_value=0, max_value=10, value=0, key="watch_grade_new")

        beyazperde_link_original = df.iloc[0, 14] if not df.empty else ""
        col_original.text_input("Beyazperde Link", value=beyazperde_link_original, disabled=True, key="beyazperde_link_original")
        col_new.text_input("New Beyazperde Link", value="", key="beyazperde_link_new")


        # Function to update the database
        def update_record():
            update_counter = 0
            update_syntax_middle = ""
            update_syntax_middle_values = []
            
            #new_original_title = st.session_state["original_title_new"]

            if (
                st.session_state["original_title_original"] != st.session_state["original_title_new"]
                and st.session_state["original_title_new"] not in ["", None]
            ):
                update_counter += 1
                update_syntax_middle = update_syntax_middle + " ,ORIGINAL_TITLE = ?"
                update_syntax_middle_values.append(st.session_state["original_title_new"])

            if (
                st.session_state["primary_title_original"] != st.session_state["primary_title_new"]
                and st.session_state["primary_title_new"] not in ["", None]
            ):
                update_counter += 1
                update_syntax_middle = update_syntax_middle + " ,PRIMARY_TITLE = ?"
                update_syntax_middle_values.append(st.session_state["primary_title_new"])

                st.write(f"update_counter: {update_counter}")
                
                if update_counter > 0:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    update_syntax_start = "UPDATE MAIN_DATA SET ID = ID" 
                    update_syntax_end = " WHERE 1=1 AND ID = ?"
                    
                    update_syntax_final = update_syntax_start + "".join(update_syntax_middle) + update_syntax_end
                    update_syntax_middle_values.append(st.session_state["id_new"])  

                    st.write(f"update_syntax: {update_syntax_final}")
                    st.write(f"update_syntax_middle_values: {update_syntax_middle_values}")


                    try:
                        cursor.execute(update_syntax_final, update_syntax_middle_values)
                        conn.commit()
                        st.success("✅ Database updated successfully!")
                    except sqlite3.Error as e:
                        st.error(f"Database update error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.toast("There are no changes to update")
            else:
                st.toast("There are no changes to update")


        st.button("Update Database", key="update_database", on_click=update_record)



    

    st.dataframe(df)















