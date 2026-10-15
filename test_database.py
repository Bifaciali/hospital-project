"""
Модуль с тестами для функций работы с базой данных.
"""
import unittest
import sqlite3
import os


class TestDatabase(unittest.TestCase):
    """Тесты для функций работы с БД поликлиники."""

    def setUp(self):
        """
        Выполняется ПЕРЕД каждым тестом.
        Создаёт чистую тестовую базу данных.
        """
        # Удаляем старую тестовую БД, если она есть
        if os.path.exists('test_hospital.db'):
            os.remove('test_hospital.db')

        # Создаём новую
        self.conn = sqlite3.connect('test_hospital.db')
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                year INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                doctor_card TEXT UNIQUE NOT NULL,
                speciality TEXT,
                phone TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE records (
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

        self.conn.commit()

    def tearDown(self):
        """
        Выполняется ПОСЛЕ каждого теста.
        Закрывает соединение и удаляет тестовую БД.
        """
        self.conn.close()
        if os.path.exists('test_hospital.db'):
            os.remove('test_hospital.db')

    # ==========================================
    # ТЕСТЫ ДЛЯ ТАБЛИЦЫ PATIENTS
    # ==========================================

    def test_add_patient(self):
        """Проверяет добавление пациента в БД."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            ('Смирнов', 'Алексей', 'Грипп', 1990)
        )
        self.conn.commit()

        cursor.execute("SELECT * FROM patients WHERE last_name = 'Смирнов'")
        patient = cursor.fetchone()

        self.assertIsNotNone(patient, "Пациент должен быть найден в БД")
        self.assertEqual(patient[1], 'Смирнов')
        self.assertEqual(patient[2], 'Алексей')
        self.assertEqual(patient[3], 'Грипп')
        self.assertEqual(patient[4], 1990)

    def test_patient_count(self):
        """Проверяет количество пациентов в БД."""
        cursor = self.conn.cursor()
        patients = [
            ('Пациент 1', 'Имя 1', 'Диагноз 1', 2000),
            ('Пациент 2', 'Имя 2', 'Диагноз 2', 2001),
            ('Пациент 3', 'Имя 3', 'Диагноз 3', 2002),
        ]
        cursor.executemany(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            patients
        )
        self.conn.commit()

        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]

        self.assertEqual(count, 3, "В БД должно быть 3 пациента")

    def test_delete_patient(self):
        """Проверяет удаление пациента."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            ('Тестовый', 'Пациент', 'Тестовый диагноз', 2024)
        )
        self.conn.commit()
        patient_id = cursor.lastrowid

        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        self.conn.commit()

        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()

        self.assertIsNone(patient, "Пациент должен быть удалён")

    # ==========================================
    # ТЕСТЫ ДЛЯ ТАБЛИЦЫ DOCTORS
    # ==========================================

    def test_add_doctor(self):
        """Проверяет добавление врача."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO doctors (last_name, first_name, doctor_card, speciality, phone) VALUES (?, ?, ?, ?, ?)",
            ('Иванов', 'Иван', 'ВР-001', 'Терапевт', '+7-900-111-11-11')
        )
        self.conn.commit()

        cursor.execute("SELECT * FROM doctors WHERE doctor_card = 'ВР-001'")
        doctor = cursor.fetchone()

        self.assertIsNotNone(doctor)
        self.assertEqual(doctor[1], 'Иванов')
        self.assertEqual(doctor[4], 'ВР-001')

    def test_unique_doctor_card(self):
        """Проверяет, что номер карточки врача уникален."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO doctors (last_name, first_name, doctor_card) VALUES (?, ?, ?)",
            ('Иванов', 'Иван', 'ВР-001')
        )
        self.conn.commit()

        # Попытка добавить второго врача с такой же карточкой
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO doctors (last_name, first_name, doctor_card) VALUES (?, ?, ?)",
                ('Петров', 'Петр', 'ВР-001')
            )

    # ==========================================
    # ТЕСТЫ ДЛЯ ТАБЛИЦЫ RECORDS
    # ==========================================

    def test_admit_patient(self):
        """Проверяет оформление поступления пациента."""
        cursor = self.conn.cursor()

        # Добавляем пациента и врача
        cursor.execute(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            ('Смирнов', 'Алексей', 'Грипп', 1990)
        )
        patient_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO doctors (last_name, first_name, doctor_card) VALUES (?, ?, ?)",
            ('Иванов', 'Иван', 'ВР-001')
        )
        doctor_id = cursor.lastrowid

        # Оформляем поступление
        cursor.execute(
            "INSERT INTO records (patient_id, doctor_id, date_of_receipt, release_date) VALUES (?, ?, ?, ?)",
            (patient_id, doctor_id, '2026-09-01', '2026-10-01')
        )
        self.conn.commit()

        cursor.execute("SELECT COUNT(*) FROM records")
        count = cursor.fetchone()[0]

        self.assertEqual(count, 1, "Должна быть 1 запись о лечении")

    def test_discharge_patient(self):
        """Проверяет оформление выписки пациента."""
        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            ('Тестовый', 'Пациент', 'Диагноз', 2024)
        )
        patient_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO doctors (last_name, first_name, doctor_card) VALUES (?, ?, ?)",
            ('Иванов', 'Иван', 'ВР-001')
        )
        doctor_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO records (patient_id, doctor_id, date_of_receipt, release_date) VALUES (?, ?, ?, ?)",
            (patient_id, doctor_id, '2026-09-01', '2026-10-01')
        )
        record_id = cursor.lastrowid
        self.conn.commit()

        # Оформляем выписку
        cursor.execute(
            "UPDATE records SET discharge_date = ?, status = 'выписан' WHERE id = ?",
            ('2026-09-15', record_id)
        )
        self.conn.commit()

        cursor.execute("SELECT discharge_date FROM records WHERE id = ?", (record_id,))
        discharge_date = cursor.fetchone()[0]

        self.assertEqual(discharge_date, '2026-09-15')


if __name__ == '__main__':
    unittest.main()

class TestSearch(unittest.TestCase):
    """Тесты для поиска данных."""

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')  # БД в оперативной памяти
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                year INTEGER
            )
        ''')
        patients = [
            ('Иванов', 'Иван', 'Грипп', 1990),
            ('Петров', 'Пётр', 'Грипп', 1985),
            ('Сидоров', 'Сидор', 'Ангина', 2000),
        ]
        cursor.executemany(
            "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
            patients
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_search_by_diagnosis_flu(self):
        """Поиск пациентов с гриппом."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", ('%Грипп%',))
        patients = cursor.fetchall()

        self.assertEqual(len(patients), 2, "Должно быть 2 пациента с гриппом")

    def test_search_by_diagnosis_not_found(self):
        """Поиск несуществующего диагноза."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", ('%Бронхит%',))
        patients = cursor.fetchall()

        self.assertEqual(len(patients), 0, "Пациентов с бронхитом нет в БД")
