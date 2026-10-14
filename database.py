"""
Модуль для работы с базой данных "Поликлиника".
Автор: Bifaciali.
Версия 2.0 - обновлённая версия.
"""
import sqlite3

def delete_doctor(doctor_id):
    """
    Удаляет врача из базы данных по ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    if cursor.rowcount:
        print(f"Врач с ID {doctor_id} удалён.")
    else:
        print(f"Врач с ID {doctor_id} не найден.")
    conn.close()
