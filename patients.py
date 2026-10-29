import sqlite3
from database import get_connection


def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY last_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_patient_by_id(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def search_patients_by_diagnosis(diagnosis):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", (f'%{diagnosis}%',))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_patient(last_name, first_name, diagnosis, year=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            (last_name, first_name, diagnosis, year)
        )
        conn.commit()
        patient_id = cursor.lastrowid
        return patient_id
    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
        return None
    finally:
        conn.close()


def update_patient(patient_id, **fields):
    if not fields:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    updates = [f"{k} = ?" for k in fields.keys()]
    values = list(fields.values()) + [patient_id]
    try:
        cursor.execute(
            f"UPDATE patients SET {', '.join(updates)} WHERE id = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def count_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]
    conn.close()
    return count
