import streamlit as st

st.title("📺 TV Shows")
st.write("Keep track of your favorite TV series!")

# Example: Display a sample TV show list
tv_shows = ["Breaking Bad", "Stranger Things", "The Witcher"]
for show in tv_shows:
    st.markdown(f"- 📺 {show}")
