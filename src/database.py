import sqlite3

def initialising_db():
    connect = sqlite3.connect("app_database.db")
    cursor = connect.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        event_tpes TEXT,
        app_name TEXT,
        duration INTEGER,
        key_count INTEGER,
        mouse_count INTEGER,
        extra TEXT
    )
    """)
    connect.commit()
    connect.close()
