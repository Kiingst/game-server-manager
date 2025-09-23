import sqlite3
from pathlib import Path



def _init_db(path_to_db="users_database.db"):

    conn = sqlite3.connect(path_to_db)
    conn.row_factory = sqlite3.Row
    conn.execute(""" CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        """)

    
    
