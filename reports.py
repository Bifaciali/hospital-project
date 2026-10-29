from datetime import datetime
from database import get_connection


def get_overdue_patients():
    today = datetime.now().date()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            patients.last_name || ' ' || patients.first_name AS patient_name,
            patients.diagnosis,
            doctors.last_name || ' ' || doctors.first_name AS doctor_name,
            records.release_date,
            julianday(?) - julianday(records.release_date) AS days_overdue
        FROM records
        JOIN patients ON records.patient_id = patients.id
        JOIN doctors ON records.doctor_id = doctors.id
        WHERE records.discharge_date IS NULL
          AND records.release_date < ?
        ORDER BY days_overdue DESC
    ''', (today, today))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_most_frequent_patients(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            patients.last_name,
            patients.first_name,
            COUNT(records.id) AS record_count
        FROM patients
        LEFT JOIN records ON patients.id = records.patient_id
        GROUP BY patients.id
        ORDER BY record_count DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_hospital_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM records WHERE discharge_date IS NULL")
    active_records = cursor.fetchone()[0]

    today = datetime.now().date()
    cursor.execute(
        "SELECT COUNT(DISTINCT patient_id) FROM records WHERE discharge_date IS NULL AND release_date < ?",
        (today,)
    )
    overdue_patients = cursor.fetchone()[0]

    conn.close()
    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "active_records": active_records,
        "overdue_patients": overdue_patients
    }
