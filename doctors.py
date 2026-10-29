import sqlite3
from database import get_connection


def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors ORDER BY last_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_doctor_by_id(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_doctor(last_name, first_name, doctor_card, speciality=None, phone=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO doctors (last_name, first_name, doctor_card, speciality, phone) VALUES (?, ?, ?, ?, ?)",
            (last_name, first_name, doctor_card, speciality, phone)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Врач с карточкой {doctor_card} уже существует")
        return None
    finally:
        conn.close()


def update_doctor(doctor_id, **fields):
    if not fields:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    updates = [f"{k} = ?" for k in fields.keys()]
    values = list(fields.values()) + [doctor_id]
    try:
        cursor.execute(
            f"UPDATE doctors SET {', '.join(updates)} WHERE id = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
