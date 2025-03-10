import streamlit as st

st.title("Data Entry")

imdb_link = st.text_input("IMDb Link", "https://www.imdb.com/title/")
original_title = st.text_input("Original Title")
primary_title = st.text_input("Primary Title")
status = st.selectbox('Status', ["POTENTIAL", "TO BE WATCHED", "MAYBE","N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"]) #This function is used to display a select widget.
#st.write("The current movie title is", title)







left, middle, right = st.columns(3)
if left.button("Insert Record", use_container_width=True):
    left.markdown("You clicked the insert record button.")
if middle.button("Clear Form", use_container_width=True):
    middle.markdown("You clicked the clear form button.")
if right.button("Unknown Button", use_container_width=True):
    right.markdown("You clicked the Unknown button.")


# Button tıklandığında sqlite database içine veri eklemesi sağlanacak: https://docs.streamlit.io/develop/concepts/design/buttons