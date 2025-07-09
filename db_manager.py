import sqlite3

DB_NAME = "bank.db"

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
            acc_num TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            acc_num TEXT PRIMARY KEY,
            pin TEXT NOT NULL
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_num TEXT,
            type TEXT,
            amount REAL,
            time TEXT
        )""")
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
