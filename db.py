import sqlite3

DATABASE_NAME = "eventpulse.db"


def initialize_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT NOT NULL,

            file_name TEXT NOT NULL,

            action TEXT NOT NULL

        )
    """)

    connection.commit()
    connection.close()


def save_event(time, file_name, action):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO history
        (
            time,
            file_name,
            action
        )

        VALUES (?, ?, ?)

    """, (time, file_name, action))

    connection.commit()

    connection.close()


def get_history():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""

        SELECT

            time,

            file_name,

            action

        FROM history

        ORDER BY id DESC

    """)

    history = cursor.fetchall()

    connection.close()

    return history


def clear_history():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""

        DELETE FROM history

    """)

    connection.commit()

    connection.close()