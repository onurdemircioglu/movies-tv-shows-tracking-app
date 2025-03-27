import streamlit as st

# Sample Data
shows = {
    "Breaking Bad": [False] * 13,   # False means 'not watched'
    "Stranger Things": [False] * 13,
}

# Select a TV Show
selected_show = st.selectbox("Select a TV Show:", list(shows.keys()))

# Display Episodes
with st.expander(f"{selected_show} - Episodes"):
    for i in range(len(shows[selected_show])):
        shows[selected_show][i] = st.checkbox(f"Episode {i+1}", value=shows[selected_show][i], key=f"{selected_show}_ep{i+1}")

# Save Updates Button (You'd store updates in a database)
if st.button("Save Progress"):
    st.success("✅ Progress saved successfully!")
