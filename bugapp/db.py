import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "bugs.db"

def get_connection():
    # returns a connection with rows accessible by name
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
