import streamlit as st

st.header('st.multiselect')

st.multiselect('Choose a planet', ['Jupiter', 'Mars', 'Neptune']) #This function is used to display a multiselect widget.

options = st.multiselect(
     'What are your favorite colors',
     ['Green', 'Yellow', 'Red', 'Blue'],
     ['Yellow', 'Green'])

st.write('You selected:', options)