import sys
sys.path.append(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app")

import streamlit as st
import pandas as pd
import sqlite3
import my_functions

st.title("Update Record")

db_path = r"C:\Users\onur\anaconda3\envs\movies_streamlit\app\movies_tv_shows.db"

# Load data
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
df = pd.read_sql_query(
    """SELECT ID, IMDB_TT, TYPE,
    ORIGINAL_TITLE, PRIMARY_TITLE,
    RELEASE_YEAR, 
    STATUS, SCORE, SCORE_DATE,
    GENRES, DURATION, RATING, RATING_COUNT,
    WATCH_GRADE, BEYAZPERDE_LINK
    FROM MAIN_DATA""", conn)
original_df = df.copy()
conn.close()

# UI Components
imdb_link = st.text_input("IMDb Link", value="https://www.imdb.com/title/", key="imdb_link")
find_record_button = st.button("Find Record", key="find_record")

if "edited_df" not in st.session_state:
    st.session_state.edited_df = pd.DataFrame()

if find_record_button:
    imdb_link = st.session_state.get("imdb_link", "")
    obj = my_functions.MyClass()

    if "/title/tt" in imdb_link:
        imdb_in = obj.imdb_converter(imdb_link, "in")
        st.session_state.edited_df = df[df["IMDB_TT"] == imdb_in]

if not st.session_state.edited_df.empty:
    edited_df = st.data_editor(
        st.session_state.edited_df, 
        num_rows="fixed", 
        disabled=("ID", "IMDB_TT"), 
        key="edited_data", 
        hide_index=True
    )

    if st.button("Update Database"):
        original_df_filtered = original_df[original_df["ID"].isin(st.session_state.edited_df["ID"])]

        # Strip whitespace to prevent false changes
        cols_to_strip = ["ORIGINAL_TITLE", "GENRES"]
        for col in cols_to_strip:
            original_df_filtered[col] = original_df_filtered[col].astype(str).str.strip()
            st.session_state.edited_df[col] = st.session_state.edited_df[col].astype(str).str.strip()

        # Convert ID to int
        original_df_filtered["ID"] = original_df_filtered["ID"].astype(int)
        st.session_state.edited_df["ID"] = st.session_state.edited_df["ID"].astype(int)

        # Debug: Show normalized data before comparing
        st.write("🔍 Normalized Original DataFrame:", original_df_filtered)
        st.write("🔍 Normalized Edited DataFrame:", st.session_state.edited_df)

        # Detect changes using more robust method
        changes = ~original_df_filtered.eq(st.session_state.edited_df)

        # Open a connection once
        if changes.any().any():  # Check if at least one cell has changed
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            #updates = False

            for index, row in st.session_state.edited_df.iterrows():
                record_id = row["ID"]
                original_row = original_df_filtered.loc[original_df_filtered["ID"] == record_id]

                if original_row.empty:
                    st.error(f"⚠️ No matching record found in original_df for ID {record_id}!")
                    continue  # Skip this record

                    # Extract values and update only if changed
                    new_values = {
                        "ORIGINAL_TITLE": row["ORIGINAL_TITLE"],
                        "GENRES": row["GENRES"],
                        "RATING": row["RATING"]
                    }
                    old_values = {
                        "ORIGINAL_TITLE": original_row.iloc[0]["ORIGINAL_TITLE"],
                        "GENRES": original_row.iloc[0]["GENRES"],
                        "RATING": original_row.iloc[0]["RATING"]
                    }

                    if new_values != old_values:
                        try:
                            cursor.execute(
                                "UPDATE MAIN_DATA SET ORIGINAL_TITLE = ?, GENRES = ?, RATING = ? WHERE ID = ?",
                                (new_values["ORIGINAL_TITLE"], new_values["GENRES"], new_values["RATING"], record_id)
                            )
                            st.write(f"✅ Updated ID {record_id}: {old_values} → {new_values}")
                        except sqlite3.Error as e:
                            st.error(f"Database update error: {e}")

                conn.commit()
                conn.close()
                st.success("✅ Database updated successfully!")
            else:
                st.warning("⚠️ No changes detected!")

        conn.close()