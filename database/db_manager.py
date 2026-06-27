import sqlite3
import os
import re
import sys

def get_db_path():
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "equipment.db")

def add_equipment(asset_tag, asset_type, brand, model, serial_number,
                  status, assigned_department, purchase_date, specs):

    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO equipment (
                asset_tag, asset_type, brand, model, serial_number,
                status, assigned_to, purchase_date, specs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (asset_tag, asset_type, brand, model, serial_number,
              status, assigned_department, purchase_date, specs))
        conn.commit()


def get_all_equipment():
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipment ORDER BY id DESC")
        return cursor.fetchall()

def search_equipment(keyword):
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        search_term = f"%{keyword}%"
        cursor.execute("""
            SELECT * FROM equipment
            WHERE asset_tag LIKE ?
            OR asset_type LIKE ?
            OR brand LIKE ?
            OR assigned_to LIKE ?
            OR status LIKE ?
        """, (search_term, search_term, search_term,
              search_term, search_term))
        return cursor.fetchall()
    
def filter_by_status(status):
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM equipment WHERE status = ? ORDER BY id DESC",
            (status,)
        )

        return cursor.fetchall()
    

def update_equipment(equipment_id, asset_tag, asset_type, brand, model,
                     serial_number, status, assigned_department, purchase_date, specs):

    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE equipment SET
                asset_tag     = ?,
                asset_type    = ?,
                brand         = ?,
                model         = ?,
                serial_number = ?,
                status        = ?,
                assigned_to   = ?,
                purchase_date = ?,
                specs         = ?
            WHERE id = ?
        """, (asset_tag, asset_type, brand, model, serial_number,
              status, assigned_department, purchase_date,
              specs, equipment_id))
        conn.commit()

def delete_equipment(equipment_id):
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
        conn.commit()
        
        
def get_equipment_by_id(equipment_id):
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
        return cursor.fetchone()
    

def get_statistics():
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN status='Active' THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='Maintenance' THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='In Storage' THEN 1 ELSE 0 END)
            FROM equipment
        """)
        row = cursor.fetchone()
        return {
            "total":       row[0] or 0,
            "active":      row[1] or 0,
            "maintenance": row[2] or 0,
            "storage":     row[3] or 0,
        }
        
        
def get_next_asset_tag(prefix):
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT asset_tag FROM equipment WHERE asset_tag LIKE ?",
            (f"{prefix}-%",)
        )

        rows = cursor.fetchall()

        max_number = 0

        for row in rows:
            tag = row[0]

            match = re.search(
                rf"{prefix}-(\d+)$",
                tag
            )

            if match:
                number = int(match.group(1))
                max_number = max(
                    max_number,
                    number
                )

        return f"{prefix}-{max_number + 1:03d}"