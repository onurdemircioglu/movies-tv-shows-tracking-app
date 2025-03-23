import sqlite3
import pandas as pd
import re
from datetime import datetime

class MyClass:  # ✅ Make sure this class is at the top level
    
    @staticmethod # Due to @staticmethod addition there is no need for 'self' declaration
    def imdb_converter(imdb_url: str, in_out: str) -> str:
        if in_out == "in":
            match = re.search(r'tt\d+', imdb_url)
            return match.group() if match else None
        elif in_out == "out":
            return "https://www.imdb.com/title/" + imdb_url + "/"
        else:
            return "Error"
    
    @staticmethod
    def beyazperde_converter(beyazperde_url: str, in_out: str) -> str:
        if in_out == "in":
            beyazperde_result = beyazperde_url.replace("https://www.beyazperde.com/","")
        elif in_out == "out":
            beyazperde_result = "https://www.beyazperde.com/" + beyazperde_url
        else:
            beyazperde_result = "Error"
        
        return beyazperde_result

    
    def check_existing_record(self, imdb_tt: str):  # ✅ Added 'self'
        conn = sqlite3.connect("movies_tv_shows.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", (imdb_tt,))
        data_exist = pd.read_sql_query("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", conn, params=(imdb_tt,))

        if not data_exist.empty:  # ✅ Corrected check
            return data_exist.iloc[0, 0]  # ✅ Use iloc[0, 0] instead of data_exist[0]

        conn.close()
        return None
   
    
    def insert_new_record(self
                          ,imdb_tt: str, record_type: str, record_title_type: str
                          ,original_title: str = None, primary_title: str = None
                          ,record_status: str = None, release_year: int = None
                          ,record_score: int = None, score_date: str = None
                          ,imdb_rating: float = None
                          ,imdb_rating_count: int = None
                          # : int = Nones
                          ,imdb_genres: str = None
                          ,watch_grade: int = None
                          ):
        conn = sqlite3.connect(r"C:\Users\onur\anaconda3\envs\movies_streamlit\app\movies_tv_shows.db")
        cursor = conn.cursor()


        # Convert imdb_rating safely
        if imdb_rating in [None, '']:  
            imdb_rating = 0.0
        
        # Convert imdb_rating_count safely
        if imdb_rating_count in [None, '']:  # Check if it's None or an empty string
            imdb_rating_count = 0  # Set a default value

        # Convert release_year safely
        if release_year in [None, '']:  # Check if it's None or an empty string
            release_year = 0  # Set a default value



        # Build the insert query dynamically based on non-empty values
        columns = ["IMDB_TT"]
        values = [imdb_tt]
        
        if original_title:
            columns.append("ORIGINAL_TITLE")
            values.append(original_title)
        if primary_title:
            columns.append("PRIMARY_TITLE")
            values.append(primary_title)
        if record_type:
            columns.append("TYPE")
            values.append(record_type)
        if record_title_type:
            columns.append("TITLE_TYPE")
            values.append(record_title_type)
        if record_status:
            columns.append("STATUS")
            values.append(record_status)
        if release_year:
            columns.append("RELEASE_YEAR")
            values.append(release_year)
        if record_score:
            columns.append("SCORE")
            values.append(record_score)
        if record_status == "WATCHED" and score_date:
            columns.append("SCORE_DATE")
            values.append(score_date)
        if float(imdb_rating) > 0.0:
            columns.append("RATING")
            values.append(imdb_rating)
        if float(imdb_rating) > 0.0:
            columns.append("RATING_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if imdb_rating_count > 0:
            columns.append("RATING_COUNT")
            values.append(imdb_rating_count)
        if imdb_genres:
            columns.append("GENRES")
            values.append(imdb_genres)
        if imdb_genres:
            columns.append("GENRES_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if (record_status == "TO BE WATCHED" or record_status == "MAYBE") and watch_grade > 0:
            columns.append("WATCH_GRADE")
            values.append(watch_grade)
        if imdb_tt:
            columns.append("INSERT_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        if imdb_tt:
            columns.append("MANUAL_UPDATE_DATE")
            values.append(datetime.today().strftime("%Y-%m-%d"))
        


        placeholders = ", ".join(["?"] * len(values))  # Generates ?, ?, ?, ?
        #print(placeholders)
        #print(values)
        query = f"INSERT INTO MAIN_DATA ({', '.join(columns)}) VALUES ({placeholders})"

        # Execute the insert query
        cursor.execute(query, values)
        conn.commit()

        #st.success("✅ New record inserted successfully!")


        # Insert new record (assuming other required fields have default values)
        #cursor.execute("INSERT INTO MAIN_DATA (IMDB_TT) VALUES (?)", (imdb_tt,))
        #conn.commit()

        # Check if the record inserted and exists in the database now.
        cursor.execute("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", (imdb_tt,))
        new_record_id = cursor.fetchone()[0]
        #print("new_record_id", new_record_id)

        cursor.close()
        conn.close()

        return new_record_id
    



