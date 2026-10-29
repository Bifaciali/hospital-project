import sqlite3
import hashlib

DB_PATH = 'hospital.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
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
        status TEXT DEFAULT 'на лечении',
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        doctor_id INTEGER,
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_pass = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", admin_pass, "admin")
        )
        print("Создан пользователь по умолчанию: логин 'admin', пароль 'admin123'")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
