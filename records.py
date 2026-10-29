import sqlite3
from datetime import datetime, timedelta
from database import get_connection


def admit_patient(patient_id, doctor_id, days=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    if not patient:
        conn.close()
        return False, "Пациент не найден"

    date_of_receipt = datetime.now().date()
    release_date = date_of_receipt + timedelta(days=days)

    try:
        cursor.execute('''
        INSERT INTO records (patient_id, doctor_id, date_of_receipt, release_date, status)
        VALUES (?, ?, ?, ?, 'на лечении')
        ''', (patient_id, doctor_id, date_of_receipt, release_date))
        conn.commit()
        return True, f"Пациент поступил. Планируемая выписка: {release_date}"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()


def discharge_patient(record_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records WHERE id = ? AND discharge_date IS NULL", (record_id,))
    record = cursor.fetchone()
    if not record:
        conn.close()
        return False, "Запись не найдена или пациент уже выписан"

    today = datetime.now().date()
    try:
        cursor.execute(
            "UPDATE records SET discharge_date = ?, status = 'выписан' WHERE id = ?",
            (today, record_id)
        )
        conn.commit()
        return True, "Пациент выписан"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()


def get_all_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            records.id,
            patients.last_name || ' ' || patients.first_name AS patient_name,
            doctors.last_name || ' ' || doctors.first_name AS doctor_name,
            records.date_of_receipt,
            records.release_date,
            records.discharge_date,
            records.status
        FROM records
        JOIN patients ON records.patient_id = patients.id
        JOIN doctors ON records.doctor_id = doctors.id
        ORDER BY records.date_of_receipt DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_active_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            records.id,
            patients.last_name || ' ' || patients.first_name AS patient_name,
            doctors.last_name || ' ' || doctors.first_name AS doctor_name,
            records.date_of_receipt,
            records.release_date
        FROM records
        JOIN patients ON records.patient_id = patients.id
        JOIN doctors ON records.doctor_id = doctors.id
        WHERE records.discharge_date IS NULL
        ORDER BY records.release_date
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
