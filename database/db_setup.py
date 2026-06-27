import sqlite3
import os
import sys

def create_database():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    db_path = os.path.join(base_dir, "equipment.db")

    with sqlite3.connect(db_path) as connection:
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
                purchase_date   TEXT,
                specs           TEXT
            )
        """)
        connection.commit()
    print("Database ready.")