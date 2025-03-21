from DAO.DAO_abstract import DAO
import sqlite3
from contextlib import ContextDecorator

class SQLiteDAO(DAO, ContextDecorator):

    def __init__(self, db_name: str):
        super().__init__(db_name)

    def __enter__(self):
        self.connect()
        self.create_table()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.close()

    def connect(self):
        try:
            self.con = sqlite3.connect(self.db_name)
            self.con.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        try:
            with self.con:
                self.con.execute('''CREATE TABLE IF NOT EXISTS leaderboard(
                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Score INTEGER NOT NULL,
                    Level INTEGER NOT NULL
                )''')
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def close(self):
        try:
            if self.con:
                self.con.close()
        except sqlite3.Error as e:
            print(f'Error closing database: {e}')

    def insert(self, name: str, score: int, level: int):
        try:
            with self.con:
                self.con.execute('''INSERT INTO leaderboard(Name, Score, Level) VALUES (?,?,?)''', (name, score, level))
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return False

    def get_all(self, level: int):
        leaderboard_entries = []
        try:
            with self.con:
                cursor = self.con.execute('''SELECT Name,Score FROM leaderboard WHERE Level = ? ORDER BY 
                Score DESC''', (level,))
                rows = cursor.fetchall()

                for row in rows:
                    entry = (row['Name'], row['Score'])
                    leaderboard_entries.append(entry)

        except sqlite3.Error as e:
            print(f'Error getting data from database: {e}')

        return leaderboard_entries
