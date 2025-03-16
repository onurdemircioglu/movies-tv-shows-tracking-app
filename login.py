import streamlit as st

# Hardcoded user database (Replace with SQLite in future)
USER_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "admin"},
    "onur": {"password": "user123", "role": "user"},
}

def check_login():
    """Login page with username & password authentication."""
    
    st.title("🔐 Login Page")

    # Initialize session state for inputs
    if "input_username" not in st.session_state:
        st.session_state["input_username"] = ""
    if "input_password" not in st.session_state:
        st.session_state["input_password"] = ""

    # User input fields with unique keys, using session state to handle input values
    username = st.text_input("Username:", placeholder="Enter your username", key="input_username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="input_password")
    #confirm_password = st.text_input("Confirm Password:", type="password", key="login_confirm_password")

    # Only show login button if username and password are not already entered
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USER_CREDENTIALS[username]["role"]
            st.success(f"✅ Logged in as {username} ({st.session_state['role']})")
            st.rerun()  # Refresh page after login
        else:
            st.error("❌ Incorrect username or password.")

# ✅ Only show login if user is NOT logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    check_login()
