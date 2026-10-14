"""
Модуль для работы с базой данных "Поликлиника".
"""
import sqlite3

def get_connection():
    """Возвращает соединение с базой данных."""
    return sqlite3.connect('hospital.db')

def init_database():
    """Создаёт таблицы в базе данных."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        year INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        doctor_card TEXT UNIQUE NOT NULL,
        speciality TEXT,
        phone TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date_of_receipt DATE NOT NULL,
        release_date DATE NOT NULL,
        discharge_date DATE,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
    ''')

    conn.commit()
    conn.close()
    print("База данных инициализирована!")

if __name__ == "__main__":
    init_database()
