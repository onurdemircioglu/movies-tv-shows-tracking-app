import streamlit as st

st.title("🛠️ Admin Panel")

# Restrict access to admin users
if "logged_in" not in st.session_state or st.session_state.get("role") != "admin":
    st.error("🚫 You do not have access to this page.")
    st.stop()  # Prevent further execution

st.success("✅ Welcome, Admin! You have full access.")
st.write("🔹 This is a secure admin panel. Only admins can see this.")
