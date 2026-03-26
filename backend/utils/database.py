import sqlite3

DB_PATH = "c:\\Users\\Kevin Tran\\Desktop\\big projects\\backend\\data\\recipes.db"

def get_db_connection():
    """
    Establish a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access
    return conn

def initialize_database():
    """
    Create the recipes table if it doesn't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            confidence REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()