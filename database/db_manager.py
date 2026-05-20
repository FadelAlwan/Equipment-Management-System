import sqlite3
import os

def get_db_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "equipment.db")

def add_equipment(asset_tag, asset_type, brand, model, serial_number,
                  status, assigned_to, department, purchase_date,
                  warranty_expiry, specs, notes):

    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO equipment (
                asset_tag, asset_type, brand, model, serial_number,
                status, assigned_to, department, purchase_date,
                warranty_expiry, specs, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (asset_tag, asset_type, brand, model, serial_number,
              status, assigned_to, department, purchase_date,
              warranty_expiry, specs, notes))
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
            OR department LIKE ?
            OR status LIKE ?
        """, (search_term, search_term, search_term,
              search_term, search_term, search_term))
        return cursor.fetchall()
    

def update_equipment(equipment_id, asset_tag, asset_type, brand, model,
                     serial_number, status, assigned_to, department,
                     purchase_date, warranty_expiry, specs, notes):

    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE equipment SET
                asset_tag       = ?,
                asset_type      = ?,
                brand           = ?,
                model           = ?,
                serial_number   = ?,
                status          = ?,
                assigned_to     = ?,
                department      = ?,
                purchase_date   = ?,
                warranty_expiry = ?,
                specs           = ?,
                notes           = ?
            WHERE id = ?
        """, (asset_tag, asset_type, brand, model, serial_number,
              status, assigned_to, department, purchase_date,
              warranty_expiry, specs, notes, equipment_id))
        conn.commit()


def delete_equipment(equipment_id):
    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
        conn.commit()