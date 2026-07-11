import sqlite3

DATABASE_NAME = "eventpulse.db"


def initialize_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT,

            event TEXT,

            file_name TEXT,

            action TEXT

        )
    """)

    connection.commit()
    connection.close()


def save_event(time, event, file_name, action):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO history
        (time, event, file_name, action)

        VALUES (?, ?, ?, ?)
    """, (time, event, file_name, action))

    connection.commit()
    connection.close()