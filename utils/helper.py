import streamlit as st

page_home = st.Page("page_home.py", title="Home", icon=":material/house:")
page_movies = st.Page("page_movies.py", title="Movies", icon="🎦", url_path="movies")
page_tv_shows = st.Page("page_tv_shows.py", title="TV Shows", icon="📺", url_path="tv-shows")

# Initialize navigation
pg = st.navigation([page_home, page_movies, page_tv_shows])

# Set page config
#st.set_page_config(page_title="Movies & TV Series Tracker", page_icon="🎥")

pg.run()
# ":smiley:"
# "🎥"




st.title("🎦 Movies")
st.title("🏠 Home Page")
st.write("Track your favorite movies here!")

# Example: Display a sample movie list
movies = ["Inception", "Interstellar", "The Dark Knight"]
for movie in movies:
    st.markdown(f"- 🎬 {movie}")
    



# Authentication
def authenticate():
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == st.secrets["credentials"]["username"] and pwd == st.secrets["credentials"]["password"]:
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    authenticate()
else:
    # Navigation
    page_home = st.Page("page_home.py", title="Home", icon=":material/house:")
    page_movies = st.Page("page_movies.py", title="Movies", icon="🎦", url_path="movies")
    page_tv_shows = st.Page("page_tv_shows.py", title="TV Shows", icon="📺", url_path="tv-shows")

    pg = st.navigation([page_home, page_movies, page_tv_shows])
    pg.run()








all_data_df = pd.read_excel(r"Z:\VirtualMachinesShared\movies_for_github.xlsx", header=0, index_col=0, thousands=",", usecols=("ID","Type","IMDb TT","Original Title","Primary Title","Release Year","Status","Score","Score Date","Genres","Watch Grade"))
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









If the DataFrame updates (e.g., adding/removing movies), update st.session_state.df_movies instead of reloading from the database:
st.session_state.df_movies = updated_df  # Update the stored DataFrame
This ensures smooth updates without reloading the database every time.



#all_data_df, all_movies_df, all_tv_shows_df, movies_watched_df, movies_watched_last_20_df = load_data()


# Access Data from session_state
if "all_data_df" in st.session_state:
    st.dataframe(st.session_state.all_data_df.head())  # Display the DataFrame
else:
    st.error("❌ No data available. Refresh the app to load data.")



"""if "movies_unwatched_df" in st.session_state:
    st.subheader("Unwatched Movies")
    st.dataframe(st.session_state.movies_unwatched_df)"""








Retrieve & Convert Back to List
# Fetch data from the database
cursor.execute("SELECT genres FROM movies WHERE title = ?", (title,))
row = cursor.fetchone()

if row:
    stored_genres = row[0]  # Stored as a comma-separated string
    imdb_genres_list = stored_genres.split(", ") if stored_genres else []  # Convert back to list
    st.write("Selected Genres:", imdb_genres_list)









with st.form("my_form",clear_on_submit=True):
    st.write("Inside the form")
    slider_val = st.slider("Form Slider")
    checkbox_val = st.checkbox("Form checkbox")
    #st.text_input(label="my text input label", value="my value")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")





# Visual Studio Code içinde sıfırdan environment yaratmak için New terminal seçilir
python -m venv streamlit_kanban_board
Set-ExecutionPolicy Unrestricted -Scope Process

# activate etmek için
movies_streamlit\Scripts\Activate.ps1

cd .\movies_streamlit\app\

streamlit run app.py

terminal üzerinden devam ederek kurulum da yapabiliyoruz.
pip install streamlit matplotlib pandas

streamlit cache clear

SELECT * FROM MAIN_DATA WHERE 1=1 AND IMDB_TT = 'tt7181546'
ORDER BY ORIGINAL_TITLE


pip install streamli
pip install streamlit-elements==0.1



    st.subheader("🎬 Add a Movie")

    title = st.text_input("Title", value=st.session_state["title"], key="title")
    imdb_tt = st.text_input("IMDB ID", value=st.session_state["imdb_tt"], key="imdb_tt")
    imdb_rating = st.number_input("IMDB Rating", min_value=0.0, max_value=10.0, step=0.1, 
                                  value=st.session_state["imdb_rating"], key="imdb_rating")
    watch_date = st.date_input("Watch Date", value=st.session_state["watch_date"], key="watch_date")
    
    record_status = st.radio("Status", 
                             ["POTENTIAL", "TO BE WATCHED", "MAYBE", "N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"], 
                             index=["POTENTIAL", "TO BE WATCHED", "MAYBE", "N2WATCH", "IN PROGRESS", "WATCHED", "DROPPED"]
                             .index(st.session_state["record_status"]), key="record_status", horizontal=True)

    imdb_genres = st.multiselect("Genres",
        ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy",
         "Film-Noir", "Game-Show", "History", "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", "Romance",
         "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller", "War", "Western"],
        default=st.session_state["imdb_genres"], key="imdb_genres")



# template ya da blog
with st.form(key='columns_in_form'):
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.selectbox(f'Make a Selection', ['click', 'or click'], key=i)
    submitted = st.form_submit_button('Submit')



# template ya da blog. chat yapılabilri bununla farklı userlar ile https://www.restack.io/docs/streamlit-knowledge-streamlit-chat-feedback-insights#clvottssx0d2d11mob1ljbmhn
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
prompt = st.chat_input("Say something")
if prompt:
    # Echo the input back to the chat
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()



left, middle, right = st.columns(3)

left.button("Insert Record", use_container_width=True, on_click=insert_new_record_process)
    #pass  # No need for extra logic here
#if left.button("Insert Record", use_container_width=True, on_click=insert_new_record):


if middle.button("Clear Form", use_container_width=True):
    clear_form()
    st.rerun()  # Refresh the page to apply changes
if right.button("Unknown Button", use_container_width=True):
    right.markdown("You clicked the Unknown button.")







blog ya da template. st.form içinde çalışmıyor bu
import streamlit as st

# Define category-wise options
category_options = {
    "Fruits": ["Apple", "Banana", "Orange", "Mango"],
    "Vegetables": ["Carrot", "Broccoli", "Spinach", "Potato"],
    "Dairy": ["Milk", "Cheese", "Yogurt"]
}

# First selection with radio buttons
selected_category = st.radio("Select Category", list(category_options.keys()), index=None)

# Second selectbox updates based on first selection
if selected_category:
    selected_item = st.selectbox("Select Item", category_options[selected_category], key="items")
    st.write("**Selected Category:**", selected_category)
    st.write("**Selected Item:**", selected_item)
else:
    st.warning("Please select a category to see items.")






https://www.sqlite.org/lang_corefunc.html#ifnull












today recommendation için

# Access stored DataFrames
if (
    "all_data_df" in st.session_state 
):


    # ************************************************ #
    # ************************************************ #
    # ************************************************ #

    # Picking a random record for recommendation
    random_pick_df = st.session_state.all_data_df.copy()

    # Filter for movies and TV shows, excluding "unknown" type
    random_pick_df = random_pick_df[random_pick_df["TYPE"].isin(["Movie", "TV Series"])]

    # Apply the given conditions
    filtered_df = random_pick_df[
        (random_pick_df["RATING"] >= 6) &  # Rating should be >= 5.5
        (random_pick_df["RATING_COUNT"] > 6000) &  # Rating count should be > 5000
        (~random_pick_df["STATUS"].isin(["TO BE WATCHED", "N2WATCH", "IN PROGRESS", "DROPPED"])) & # Status should not be in excluded statuses
        (random_pick_df["ORIGINAL_TITLE"].notna() | random_pick_df["PRIMARY_TITLE"].notna())  # At least one of ORIGINAL_TITLE or PRIMARY_TITLE should not be null
    ]

    # Check if there are any records that match the criteria
    if not filtered_df.empty:
        # Randomly select one record from the filtered data
        random_record = filtered_df.sample(n=1).iloc[0]

        # Determine the title to display
        if pd.isna(random_record["PRIMARY_TITLE"]):
            display_title = random_record["ORIGINAL_TITLE"]
        else:
            display_title = f"{random_record['ORIGINAL_TITLE']} - {random_record['PRIMARY_TITLE']}"

        # Convert RATING_COUNT to integer (remove decimal point)
        rating_count_int = int(random_record["RATING_COUNT"])

        # Convert RELEASE_YEAR to integer (remove decimal point)
        if random_record["RELEASE_YEAR"]:
            release_year_int = int(random_record["RELEASE_YEAR"])

        imdb_link_formatted = "https://www.imdb.com/title/" + str(random_record['IMDB_TT'])
        
        
        # Display the random record's information
        st.subheader(f"Today's Recommendation: {display_title}")
        #st.write(f"**IMDb Link**: {random_record['IMDB_TT']}")
        st.write(f"**IMDb Link**: {imdb_link_formatted}")
        st.write(f"**Type**: {random_record['TYPE']}")
        st.write(f"**Release Year**: {release_year_int}")
        st.write(f"**Rating**: {random_record['RATING']}")
        st.write(f"**Rating Count**: {rating_count_int}")
        st.write(f"**Status**: {random_record['STATUS']}")
        st.write(f"**Genres**: {random_record['GENRES']}")

        #st.write("movies sayfasına dataframe koyalım orada bırakalım bugün")
    else:
        st.write("No records found that match the criteria.")
        


else:
    st.warning("No data available. Please load data first.")

