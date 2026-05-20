import sqlite3
import os

def create_database():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "equipment.db")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_tag       TEXT NOT NULL UNIQUE,
            asset_type      TEXT NOT NULL,
            brand           TEXT,
            model           TEXT,
            serial_number   TEXT,
            status          TEXT DEFAULT 'Active',
            assigned_to     TEXT,
            department      TEXT,
            purchase_date   TEXT,
            warranty_expiry TEXT,
            specs           TEXT,
            notes           TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Database ready.")