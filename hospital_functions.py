"""
Модуль с функциями для поликлиники.
Содержит функции с обработкой граничных случаев.
"""
import sqlite3


def validate_year(year):
    """
    Проверяет корректность года рождения пациента.

    Args:
        year (int): год рождения

    Returns:
        bool: True, если год корректен

    Raises:
        ValueError: если год не входит в диапазон 1900-2026
    """
    if not isinstance(year, int):
        raise ValueError("Год должен быть целым числом")
    if year < 1900 or year > 2026:
        raise ValueError(f"Год {year} вне допустимого диапазона (1900-2026)")
    return True


def validate_days(days):
    """
    Проверяет корректность срока лечения.

    Args:
        days (int): срок лечения в днях

    Returns:
        bool: True, если срок корректен

    Raises:
        ValueError: если срок отрицательный или ноль
    """
    if not isinstance(days, int):
        raise ValueError("Срок лечения должен быть целым числом")
    if days <= 0:
        raise ValueError(f"Срок лечения должен быть положительным (получено {days})")
    return True


def validate_doctor_card(doctor_card):
    """
    Проверяет корректность номера карточки врача.

    Args:
        doctor_card (str): номер карточки врача

    Returns:
        bool: True, если номер корректен

    Raises:
        ValueError: если номер пустой или слишком длинный
    """
    if not doctor_card or not doctor_card.strip():
        raise ValueError("Номер карточки врача не может быть пустым")
    if len(doctor_card) > 20:
        raise ValueError(f"Номер карточки врача слишком длинный (макс. 20 символов)")
    return True


def calculate_overdue_days(release_date, discharge_date):
    """
    Вычисляет количество дней просрочки выписки.

    Args:
        release_date (str): планируемая дата выписки (YYYY-MM-DD)
        discharge_date (str): фактическая дата выписки (YYYY-MM-DD)

    Returns:
        int: количество дней просрочки (0, если не просрочено)

    Raises:
        ValueError: если даты в неверном формате
    """
    from datetime import datetime

    try:
        release = datetime.strptime(release_date, '%Y-%m-%d')
        discharged = datetime.strptime(discharge_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Даты должны быть в формате YYYY-MM-DD")

    delta = (discharged - release).days
    if delta < 0:
        return 0  # Не просрочено
    return delta


def format_diagnosis(diagnosis, max_length=30):
    """
    Форматирует диагноз для вывода.

    Args:
        diagnosis (str): диагноз пациента
        max_length (int): максимальная длина

    Returns:
        str: отформатированный диагноз

    Raises:
        ValueError: если диагноз пустой
    """
    if not diagnosis or not diagnosis.strip():
        raise ValueError("Диагноз не может быть пустым")
    if len(diagnosis) <= max_length:
        return diagnosis
    return diagnosis[:max_length - 3] + "..."
