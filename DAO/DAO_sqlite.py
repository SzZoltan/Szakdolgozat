from DAO_abstract import DAO
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
        self.con = sqlite3.connect(self.db_name)
        self.con.row_factory = sqlite3.Row

    def create_table(self):
        with self.con:
            self.con.execute('''CREATE TABLE IF NOT EXISTS leaderboard(
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Score INTEGER NOT NULL,
                Level INTEGER NOT NULL
            )''')

    def close(self):
        if self.con:
            self.con.close()

    def insert(self, data):
        pass

    def get_all(self):
        pass
