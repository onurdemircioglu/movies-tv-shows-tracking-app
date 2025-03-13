import time
import sys
sys.path.append(r"C:\Users\onur\anaconda3\envs\movies_streamlit2\app")

import streamlit as st
import my_functions

#print(dir(my_functions))

st.title("Data Entry")



def insert_new_record_process():
    imdb_link = st.session_state.get("imdb_link", "")
    obj = my_functions.MyClass()
    
    # Convert imdb link to tt format
    if "/title/" in imdb_link:
        imdb_in = obj.imdb_converter(imdb_link, "in")
        #st.write(imdb_in)

        # Check if the record (imdb_tt) already exists
        toast_message = st.toast("Checking if the record already exists")
        time.sleep(5) # Actually I don't need this, it looks better with toast message :) It will be deleted later
        #TODO: Bazı toast mesajları kalabilir ancak time.sleep kalkacak
        record_exist = obj.check_existing_record(imdb_in)
        
        # If the record doesn't exist it returns NoneType.
        if record_exist != None:
            #st.write(f"Record already exists, Id = {record_exist}")
            toast_message = st.toast(f"Record already exists, Id = {record_exist}")
        else: # returns COUNT(*) = 0 
            #st.write("Else case")
            toast_message = st.toast(f"Record doesn't exist, insert process started")
            time.sleep(5)
            
            # Inserting new record
            new_record_result = obj.insert_new_record(imdb_in)

            if new_record_result > 0:
                toast_message = st.toast(f"✅ Successfully inserted record, ID: {new_record_result}")
            else:
                toast_message = st.warning("Something wrong")

            
            



    
    
    # Create an instance of MyClass before calling the function
    
    
    #record_exists = obj.check_existing_record()  # ✅ This should work!
    #print(type(record_exists))
    #print(record_exists)
    #if record_exists > 0:
        #st.toast(f"Record already exists, ID >> {record_exists}")
        

    

#imdb_link = st.text_input("IMDb Link", "https://www.imdb.com/title/")
st.text_input("IMDb Link", "https://www.imdb.com/title/", key="imdb_link")
original_title = st.text_input("Original Title")
primary_title = st.text_input("Primary Title")
status = st.selectbox('Status', ["POTENTIAL", "TO BE WATCHED", "MAYBE","N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"]) #This function is used to display a select widget.
#st.write("The current movie title is", title)


left, middle, right = st.columns(3)

left.button("Insert Record", use_container_width=True, on_click=insert_new_record_process)
    #pass  # No need for extra logic here
#if left.button("Insert Record", use_container_width=True, on_click=insert_new_record):

    #left.markdown("You clicked the insert record button.")
if middle.button("Clear Form", use_container_width=True):
    middle.markdown("You clicked the clear form button.")
if right.button("Unknown Button", use_container_width=True):
    right.markdown("You clicked the Unknown button.")