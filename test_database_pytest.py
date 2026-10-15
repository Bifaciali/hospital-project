"""
Тесты для работы с базой данных с использованием pytest.
"""
import pytest
import sqlite3
import os


@pytest.fixture
def test_db():
    """
    Фикстура: создаёт тестовую базу данных перед каждым тестом
    и удаляет её после.
    """
    db_path = 'test_pytest.db'

    # Создаём БД
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            year INTEGER
        )
    ''')
    cursor.executemany(
        "INSERT INTO patients (last_name, first_name, diagnosis, year) VALUES (?, ?, ?, ?)",
        [
            ('Иванов', 'Иван', 'Грипп', 1990),
            ('Петров', 'Пётр', 'Грипп', 1985),
            ('Сидоров', 'Сидор', 'Ангина', 2000),
        ]
    )
    conn.commit()
    conn.close()

    yield db_path  # Передаём путь к БД в тест

    # Очистка после теста
    if os.path.exists(db_path):
        os.remove(db_path)


def test_search_by_diagnosis(test_db):
    """Поиск пациентов по диагнозу."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", ('%Грипп%',))
    patients = cursor.fetchall()
    conn.close()

    assert len(patients) == 2
    assert patients[0][3] == 'Грипп'


def test_search_nonexistent_diagnosis(test_db):
    """Поиск несуществующего диагноза."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", ('%Бронхит%',))
    patients = cursor.fetchall()
    conn.close()

    assert len(patients) == 0


def test_patient_count(test_db):
    """Проверка количества пациентов."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 3


@pytest.mark.parametrize("diagnosis, expected_count", [
    ("Грипп", 2),
    ("Ангина", 1),
    ("Бронхит", 0),
    ("", 3),
])
def test_search_parametrized(test_db, diagnosis, expected_count):
    """Параметризованный поиск по диагнозу."""
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE diagnosis LIKE ?", (f'%{diagnosis}%',))
    patients = cursor.fetchall()
    conn.close()

    assert len(patients) == expected_count
