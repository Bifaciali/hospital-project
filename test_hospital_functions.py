"""
Тесты для функций поликлиники с использованием pytest.
Включают тестирование граничных случаев.
"""
import pytest
from hospital_functions import (
    validate_year,
    validate_days,
    validate_doctor_card,
    calculate_overdue_days,
    format_diagnosis,
)


# ==========================================
# ТЕСТЫ ДЛЯ validate_year
# ==========================================

def test_validate_year_valid():
    """Проверяет корректный год."""
    assert validate_year(1950) is True
    assert validate_year(2000) is True
    assert validate_year(2026) is True


def test_validate_year_too_old():
    """Граничный случай: год слишком старый."""
    with pytest.raises(ValueError):
        validate_year(1899)


def test_validate_year_too_new():
    """Граничный случай: год из будущего."""
    with pytest.raises(ValueError):
        validate_year(2027)


def test_validate_year_not_integer():
    """Граничный случай: год — не число."""
    with pytest.raises(ValueError):
        validate_year("1990")


@pytest.mark.parametrize("year", [1900, 1930, 1950, 1990, 2010, 2026])
def test_validate_year_boundaries(year):
    """Параметризованный тест: проверка границ диапазона."""
    assert validate_year(year) is True


# ==========================================
# ТЕСТЫ ДЛЯ validate_days
# ==========================================

def test_validate_days_valid():
    """Проверяет корректный срок лечения."""
    assert validate_days(1) is True
    assert validate_days(100) is True


def test_validate_days_zero():
    """Граничный случай: ноль дней."""
    with pytest.raises(ValueError):
        validate_days(0)


def test_validate_days_negative():
    """Граничный случай: отрицательный срок."""
    with pytest.raises(ValueError):
        validate_days(-5)


def test_validate_days_float():
    """Граничный случай: дробное число."""
    with pytest.raises(ValueError):
        validate_days(1.5)


# ==========================================
# ТЕСТЫ ДЛЯ validate_doctor_card
# ==========================================

def test_validate_doctor_card_valid():
    """Проверяет корректный номер карточки."""
    assert validate_doctor_card("ВР-001") is True
    assert validate_doctor_card("12345") is True


def test_validate_doctor_card_empty():
    """Граничный случай: пустая строка."""
    with pytest.raises(ValueError):
        validate_doctor_card("")


def test_validate_doctor_card_whitespace():
    """Граничный случай: только пробелы."""
    with pytest.raises(ValueError):
        validate_doctor_card("   ")


def test_validate_doctor_card_none():
    """Граничный случай: None."""
    with pytest.raises(ValueError):
        validate_doctor_card(None)


def test_validate_doctor_card_too_long():
    """Граничный случай: слишком длинный номер."""
    with pytest.raises(ValueError):
        validate_doctor_card("А" * 21)


# ==========================================
# ТЕСТЫ ДЛЯ calculate_overdue_days
# ==========================================

def test_calculate_overdue_days_not_overdue():
    """Пациент выписан раньше срока."""
    assert calculate_overdue_days("2026-10-01", "2026-09-25") == 0


def test_calculate_overdue_days_on_time():
    """Пациент выписан в срок."""
    assert calculate_overdue_days("2026-10-01", "2026-10-01") == 0


def test_calculate_overdue_days_overdue():
    """Выписка просрочена на 5 дней."""
    assert calculate_overdue_days("2026-10-01", "2026-10-06") == 5


def test_calculate_overdue_days_long_overdue():
    """Выписка просрочена на 30 дней."""
    assert calculate_overdue_days("2026-10-01", "2026-10-31") == 30


def test_calculate_overdue_days_invalid_format():
    """Граничный случай: неверный формат даты."""
    with pytest.raises(ValueError):
        calculate_overdue_days("01.10.2026", "2026-10-06")


@pytest.mark.parametrize("release, discharged, expected", [
    ("2026-10-01", "2026-09-30", 0),
    ("2026-10-01", "2026-10-01", 0),
    ("2026-10-01", "2026-10-02", 1),
    ("2026-10-01", "2026-10-10", 9),
    ("2026-10-01", "2026-11-01", 31),
])
def test_calculate_overdue_days_parametrized(release, discharged, expected):
    """Параметризованный тест для расчёта просрочки."""
    assert calculate_overdue_days(release, discharged) == expected


# ==========================================
# ТЕСТЫ ДЛЯ format_diagnosis
# ==========================================

def test_format_diagnosis_short():
    """Короткий диагноз не обрезается."""
    assert format_diagnosis("Грипп") == "Грипп"


def test_format_diagnosis_exact_length():
    """Диагноз ровно 30 символов."""
    diagnosis = "А" * 30
    assert format_diagnosis(diagnosis) == diagnosis


def test_format_diagnosis_long():
    """Длинный диагноз обрезается."""
    diagnosis = "Острая респираторная вирусная инфекция с осложнениями"
    result = format_diagnosis(diagnosis)
    assert len(result) == 30
    assert result.endswith("...")


def test_format_diagnosis_empty():
    """Граничный случай: пустой диагноз."""
    with pytest.raises(ValueError):
        format_diagnosis("")


def test_format_diagnosis_whitespace():
    """Граничный случай: только пробелы."""
    with pytest.raises(ValueError):
        format_diagnosis("   ")
