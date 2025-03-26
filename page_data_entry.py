import time
import sys
sys.path.append(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app")

import streamlit as st
import my_functions

#print(dir(my_functions))

st.title("Data Entry")




def insert_new_record_process():
    #st.write("insert_new_record_process")
    #pass
    
    imdb_link = st.session_state.get("imdb_link", "")
    obj = my_functions.MyClass()
    
    # Convert imdb link to tt format
    if "/title/tt" in imdb_link:
        imdb_in = obj.imdb_converter(imdb_link, "in")
        #st.write(imdb_in)

        # Check if the record (imdb_tt) already exists
        #toast_message = st.toast("Checking if the record already exists")
        #time.sleep(5) # Actually I don't need this, it looks better with toast message :) It will be deleted later
        record_exist = obj.check_existing_record(imdb_in)
        
        # If the record doesn't exist it returns NoneType.
        if record_exist != None:
            #st.write(f"Record already exists, Id = {record_exist}")
            toast_message = st.toast(f"Record already exists, Id = {record_exist}")
        else: # returns COUNT(*) = 0 
            #st.write("Else case")
            #toast_message = st.toast(f"Record doesn't exist, insert process started")
            #time.sleep(5)

            # Precheck - validation
            if record_status != "WATCHED" and (record_score != "" or record_score == "0"):
                st.toast("Status and Score values are inconsistent 1")
            elif record_status == "WATCHED" and (record_score == "" or record_score == None or record_score == "0"):
                st.toast("Status and Score values are inconsistent 3")
            elif record_status == "WATCHED" and (score_date == "" or score_date == None):
                st.toast("Status and Score values are inconsistent 4")
            else:

                # Convert selected genres to a single comma-separated string because st.multiselect widget returns a list
                imdb_genres_str = ", ".join(imdb_genres)

                # Inserting new record
                new_record_result = obj.insert_new_record(
                    imdb_in
                    ,record_type, record_title_type
                    ,original_title, primary_title
                    ,record_status, release_year
                    ,record_score, score_date
                    ,imdb_rating, imdb_rating_count, imdb_genres_str
                    ,watch_grade
                    )

                if new_record_result > 0:
                    toast_message = st.toast(f"✅ Successfully inserted record, ID: {new_record_result}")
                else:
                    toast_message = st.warning("Something is wrong")
    else:
        st.toast("It is not a valid IMDb title link")



if "form_loaded" not in st.session_state:
    st.session_state["form_loaded"] = False

#Loading the Form:
if not st.session_state["form_loaded"]:
    if st.button("Load Form"):
        st.session_state["form_loaded"] = True
        st.rerun()
else:
    st.write("Here's your form!")
    with st.form(key="data_entry_form",border=True):
        
        title_type_options = {
            "Movie": ["Movie", "Short", "TV Movie", "TV Special", "Video", "Unknown"],
            "TV Series": ["TV Series", "TV Mini Series", "Unknown"],
            "Unknown": ["Unknown"]
            }
        # Get unique values
        unique_title_type_options = sorted(set(sum(title_type_options.values(), [])))

        status_options = ["POTENTIAL", "TO BE WATCHED", "MAYBE", "N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"]


        imdb_link = st.text_input("IMDb Link", value="https://www.imdb.com/title/", key="imdb_link")
        record_type = st.radio(
          "Select Type",
          #["Movie", "TV Series", "Unknown"],
          list(title_type_options.keys()),
          horizontal=True,  # Makes options appear inline
          index=2,  # Default: "Unknown"
          key="record_type"
          )
        
        # If this is in the st.form it doesn't dynamically update. (If it is a standalone or outside the form then it does)
        record_title_type = st.selectbox(
          "Select Title Type",
          unique_title_type_options,
          index=unique_title_type_options.index("Unknown"),
          key="record_title_type"
          )

        original_title = st.text_input("Original Title", key="original_title")
        primary_title = st.text_input("Primary Title", key="primary_title")
        record_status = st.radio(
          "Select Status",
          #["POTENTIAL", "TO BE WATCHED", "MAYBE", "N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"],
          status_options,
          horizontal=True,  # Makes options appear inline
          index=0,  # Default: "POTENTIAL"
          key="record_status"
          )
        release_year = st.number_input("Release Year", key="release_year", value=None, min_value=1888, max_value=st.session_state.current_year)
        record_score = st.text_input("Score", key="record_score") # It is define as text_input because when it is number_input min_valus is automatically 0 or 0.00
        score_date = st.date_input("Score Date", key="score_date") # It is default value is today. While inserting into database it is handled as if record_status == "WATCHED" and score_date:
        imdb_rating = st.number_input("IMDb Rating", key="imdb_rating", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
        imdb_rating_count = st.number_input("IMDb Rating Count", min_value=0, value=0, step=1, format="%d", key="imdb_rating_count")
        imdb_genres = st.multiselect(
               'Genres',
               ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show", "History",
               "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"], key="imdb_genres")
        watch_grade = st.number_input("Watch Grade", key="watch_grade", min_value=0, max_value=10)

        submitted = st.form_submit_button("Insert Record")

        #st.form_submit_button(label="Submit", help=None, on_click=None, args=None, kwargs=None, *, type="secondary", icon=None, disabled=False, use_container_width=False)
        if submitted:
            st.write(imdb_rating_count)
            insert_new_record_process()
            #st.rerun()
            
     

#Resetting the Form:
if st.button("Clear My Form"): # Inspired by https://discuss.streamlit.io/t/solution-how-to-reset-a-streamlit-form-when-clear-on-submit-isnt-an-option/87508
    # Remove the key that shows the form
    del st.session_state["form_loaded"]
    st.rerun()