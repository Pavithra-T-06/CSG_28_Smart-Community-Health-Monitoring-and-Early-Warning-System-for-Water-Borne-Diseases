import sqlite3
from datetime import datetime

DB_NAME = "water_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community TEXT,
            ph REAL,
            turbidity REAL,
            tds REAL,
            coliform REAL,
            rainfall REAL,
            temperature REAL,
            risk TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_data(community, ph, turbidity, tds, coliform, rainfall, temperature, risk):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO water_data 
        (community, ph, turbidity, tds, coliform, rainfall, temperature, risk, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (community, ph, turbidity, tds, coliform, rainfall, temperature, risk, timestamp))

    conn.commit()
    conn.close()


def fetch_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM water_data ORDER BY timestamp DESC")
    data = cursor.fetchall()

    conn.close()
    return data


def clear_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM water_data")

    conn.commit()
    conn.close()
    
def delete_record(record_id):
    import sqlite3
    conn = sqlite3.connect("water_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM water_data WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def delete_by_community(community):
    import sqlite3
    conn = sqlite3.connect("water_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM water_data WHERE community = ?", (community,))
    conn.commit()
    conn.close()


def delete_filtered(records_ids):
    import sqlite3
    conn = sqlite3.connect("water_data.db")
    cursor = conn.cursor()

    cursor.executemany(
        "DELETE FROM water_data WHERE id = ?",
        [(rid,) for rid in records_ids]
    )

    conn.commit()
    conn.close()