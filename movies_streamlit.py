import streamlit as st
import pandas as pd


pd.options.display.float_format = '{:.0f}'.format

st.header("Movies & TV Series Tracking App")



@st.cache_data  # 👈 Add the caching decorator
def load_data():
    all_data_df = pd.read_excel("movies_for_github.xlsx", header=0, index_col=0, thousands=",", usecols=("ID","Type","IMDb TT","Original Title","Primary Title","Release Year","Status","Score","Score Date","Genres","Watch Grade"))
    # nrows=1000, 

    # Type Conversions
    all_data_df["Score Date"] = pd.to_datetime(all_data_df["Score Date"]).dt.strftime("%Y-%m-%d")

    
    # Movies
    all_movies_df = all_data_df[all_data_df["Type"] == "Movie"]
    
    # TV Shows
    all_tv_shows_df = all_data_df[all_data_df["Type"] == "TV Series"]

    
    # Release Year alanını sayısal hale gösterme denemelerimiz - çalışmadı
    #all_data_df["Release Year"] = pd.to_numeric(all_data_df["Release Year"], errors="coerce")
    #all_data_df["Release Year"] = all_data_df["Release Year"].astype(str).str.replace(",", "").astype(int)

    # Watched Movies
    movies_watched_df = all_movies_df[all_movies_df["Status"] == "WATCHED"]
    temp_sorting_df = movies_watched_df.sort_values(by="Score Date", ascending=False)
    
    movies_watched_last_20_df = temp_sorting_df.head(20)

    return all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, movies_watched_last_20_df

# Create dataframes from the function
all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, movies_watched_last_20_df = load_data()

###############################################################################
#Metric calculations - Start
###############################################################################

# Get the current year and month
current_year = pd.to_datetime('today').year
current_month = pd.to_datetime('today').month

###############################################################################
#Metric calculations - End
###############################################################################



###############################################################################
#Start building Streamlit App
###############################################################################

add_sidebar = st.sidebar.selectbox("Select a Page", ("Main","Movies", "Tv Shows", "Search"))

if add_sidebar == "Main":
    st.subheader("Metrics")

    # Convert "Score Date" to datetime if it's not already
    movies_watched_df2 = movies_watched_df.copy() # Made a copy to change the Score Date column.
    movies_watched_df2["Score Date"] = pd.to_datetime(movies_watched_df2["Score Date"])

    # All Time Watched Movies
    watched_movies_count = len(movies_watched_df)

    #This Year Watched Movies
    watched_movies_this_year_count = movies_watched_df2[(movies_watched_df2["Score Date"].dt.year == current_year) ].shape[0]

    #This Month Watched Movies
    watched_movies_this_month_count = movies_watched_df2[(movies_watched_df2['Score Date'].dt.year == current_year) & 
                            (movies_watched_df2['Score Date'].dt.month == current_month)].shape[0]
   
    st.metric(label = "All Time Watched Movies", value = watched_movies_count)
    st.metric(label = "This Year Watched Movies", value = watched_movies_this_year_count)
    st.metric(label = "This Month Watched Movies", value = watched_movies_this_month_count)

if add_sidebar == "Movies":
    st.subheader("Last Watched 20 Movies")
    st.dataframe(movies_watched_last_20_df)

    movies_highest_scores = movies_watched_df[movies_watched_df["Score"] >= 70].sort_values(by="Score", ascending=False)
    st.subheader("Highest Scored Movies")
    st.dataframe(movies_highest_scores)


if add_sidebar == "Tv Shows":
    st.subheader("Active TV Shows")

    # In Progress TV Shows
    tv_shows_in_progress_df = all_tv_shows_df[all_tv_shows_df["Status"] == "IN PROGRESS"]
    st.dataframe(tv_shows_in_progress_df)

if add_sidebar == "Search":
    st.subheader("You selected Search Page")


if add_sidebar == "Test":

    # Connect to SQLite database
    conn = sqlite3.connect("my_database.db", check_same_thread=False)
    cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    conn.commit()

    # Streamlit UI
    st.title("SQLite with Streamlit")

    # **Insert Data**
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=0, step=1)

    if st.button("Add User"):
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        st.success("User added successfully!")

    # **Display Data**
    st.subheader("Users List")
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)

    # **Update Data**
    user_id = st.number_input("Enter ID to Update", min_value=1, step=1)
    new_name = st.text_input("New Name")
    new_age = st.number_input("New Age", min_value=0, step=1)

    if st.button("Update User"):
        cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (new_name, new_age, user_id))
        conn.commit()
        st.success("User updated successfully!")

    # **Delete Data**
    delete_id = st.number_input("Enter ID to Delete", min_value=1, step=1)
    if st.button("Delete User"):
        cursor.execute("DELETE FROM users WHERE id=?", (delete_id,))
        conn.commit()
        st.warning("User deleted!")

    # Close connection on exit
    conn.close()
    
