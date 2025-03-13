import sqlite3
import pandas as pd
import re

class MyClass:  # ✅ Make sure this class is at the top level
    
    @staticmethod # Due to @staticmethod addition there is no need for 'self' declaration
    def imdb_converter(imdb_url: str, in_out: str) -> str:
        if in_out == "in":
            match = re.search(r'tt\d+', imdb_url)
            return match.group() if match else None
        elif in_out == "out":
            return "https://www.imdb.com/title/" + imdb_url + "/"
    
    def check_existing_record(self, imdb_tt: str):  # ✅ Added 'self'
        conn = sqlite3.connect("movies_tv_shows.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", (imdb_tt,))
        data_exist = pd.read_sql_query("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", conn, params=(imdb_tt,))

        if not data_exist.empty:  # ✅ Corrected check
            return data_exist.iloc[0, 0]  # ✅ Use iloc[0, 0] instead of data_exist[0]

        conn.close()
        return None
   
    
    def insert_new_record(self, imdb_tt: str):
        conn = sqlite3.connect("movies_tv_shows.db")
        cursor = conn.cursor()

        # Insert new record (assuming other required fields have default values)
        cursor.execute("INSERT INTO MAIN_DATA (IMDB_TT) VALUES (?)", (imdb_tt,))
        conn.commit()

        # Check if the record inserted and exists in the database now.
        cursor.execute("SELECT ID FROM MAIN_DATA WHERE IMDB_TT = ?", (imdb_tt,))
        new_record_id = cursor.fetchone()[0]
        #print("new_record_id", new_record_id)

        cursor.close()
        conn.close()

        return new_record_id

