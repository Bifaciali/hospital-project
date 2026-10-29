from database import init_database
from patients import (
    get_all_patients, search_patients_by_diagnosis, add_patient,
    update_patient, delete_patient, count_patients
)
from doctors import (
    get_all_doctors, add_doctor, update_doctor, delete_doctor
)
from records import admit_patient, discharge_patient, get_all_records, get_active_records
from reports import get_overdue_patients, get_most_frequent_patients, get_hospital_stats


def print_patients(patients):
    if not patients:
        print(" Пациентов не найдено.")
        return
    print(f"\n{'ID':<4} {'Фамилия':<15} {'Имя':<15} {'Диагноз':<20} {'Год':<6}")
    print("-" * 70)
    for p in patients:
        print(f"{p['id']:<4} {p['last_name'][:13]:<15} {p['first_name'][:13]:<15} {p['diagnosis'][:18]:<20} {p['year'] or '-':<6}")


def print_doctors(doctors):
    if not doctors:
        print(" Врачей не найдено.")
        return
    print(f"\n{'ID':<4} {'Фамилия':<15} {'Имя':<15} {'Карточка':<12} {'Специальность':<15}")
    print("-" * 70)
    for d in doctors:
        print(f"{d['id']:<4} {d['last_name'][:13]:<15} {d['first_name'][:13]:<15} {d['doctor_card']:<12} {d['speciality'] or '-':<15}")


def print_records(records):
    if not records:
        print(" Записей не найдено.")
        return
    print(f"\n{'ID':<4} {'Пациент':<25} {'Врач':<20} {'Поступил':<12} {'Выписка':<12}")
    print("-" * 80)
    for r in records:
        print(f"{r['id']:<4} {r['patient_name'][:23]:<25} {r['doctor_name'][:18]:<20} {str(r['date_of_receipt']):<12} {str(r['release_date']):<12}")


def main():
    init_database()

    while True:
        print("\n" + "=" * 50)
        print("     СИСТЕМА УПРАВЛЕНИЯ ПОЛИКЛИНИКОЙ")
        print("=" * 50)
        print("1. Показать всех пациентов")
        print("2. Поиск пациентов по диагнозу")
        print("3. Добавить пациента")
        print("4. Удалить пациента")
        print("5. Показать всех врачей")
        print("6. Добавить врача")
        print("7. Оформить поступление")
        print("8. Оформить выписку")
        print("9. Показать все записи")
        print("10. Пациенты с просроченной выпиской")
        print("11. Частые пациенты")
        print("12. Статистика")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_patients(get_all_patients())
        elif choice == "2":
            diagnosis = input("Диагноз: ")
            print_patients(search_patients_by_diagnosis(diagnosis))
        elif choice == "3":
            last_name = input("Фамилия: ")
            first_name = input("Имя: ")
            diagnosis = input("Диагноз: ")
            year = input("Год рождения (Enter — пропустить): ")
            year = int(year) if year.isdigit() else None
            add_patient(last_name, first_name, diagnosis, year)
            print(" Пациент добавлен")
        elif choice == "4":
            print_patients(get_all_patients())
            patient_id = int(input("ID пациента для удаления: "))
            if delete_patient(patient_id):
                print("Пациент удалён")
            else:
                print(" Пациент не найден")
        elif choice == "5":
            print_doctors(get_all_doctors())
        elif choice == "6":
            last_name = input("Фамилия: ")
            first_name = input("Имя: ")
            card = input("Номер карточки: ")
            speciality = input("Специальность: ")
            phone = input("Телефон: ")
            if add_doctor(last_name, first_name, card, speciality, phone):
                print("Врач добавлен")
        elif choice == "7":
            print_patients(get_all_patients())
            patient_id = int(input("ID пациента: "))
            print_doctors(get_all_doctors())
            doctor_id = int(input("ID врача: "))
            ok, msg = admit_patient(patient_id, doctor_id)
            print(("✅ " if ok else "❌ ") + msg)
        elif choice == "8":
            print_records(get_active_records())
            record_id = int(input("ID записи для выписки: "))
            ok, msg = discharge_patient(record_id)
            print(("✅ " if ok else "❌ ") + msg)
        elif choice == "9":
            print_records(get_all_records())
        elif choice == "10":
            overdue = get_overdue_patients()
            if overdue:
                for o in overdue:
                    print(f"⚠️ {o['patient_name']} — {o['diagnosis']} (просрочка {int(o['days_overdue'])} дн.)")
            else:
                print(" Нет просроченных выписок")
        elif choice == "11":
            for p in get_most_frequent_patients():
                print(f" {p['last_name']} {p['first_name']} — {p['record_count']} записей")
        elif choice == "12":
            stats = get_hospital_stats()
            print(f" Пациентов: {stats['total_patients']}")
            print(f" Врачей: {stats['total_doctors']}")
            print(f" На лечении: {stats['active_records']}")
            print(f" Просрочена выписка: {stats['overdue_patients']}")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")


if __name__ == '__main__':
    main()
