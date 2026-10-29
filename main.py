import sys
from database import init_database
from auth import login
from patients import get_all_patients, search_patients_by_diagnosis, add_patient, delete_patient

def show_login_screen():
    print("=" * 40)
    print("   ВХОД В СИСТЕМУ 'ПОЛИКЛИНИКА'")
    print("=" * 40)
    username = input("Логин: ")
    password = input("Пароль: ")
    return login(username, password)

def menu_admin():
    print("\n--- МЕНЮ АДМИНИСТРАТОРА ---")
    print("1. Все пациенты")
    print("2. Добавить пациента")
    print("3. Удалить пациента")
    print("0. Выход")

def menu_user():
    print("\n--- МЕНЮ ВРАЧА ---")
    print("1. Список пациентов")
    print("2. Поиск по диагнозу")
    print("0. Выход")

def main():
    init_database()

    user = show_login_screen()
    if not user:
        print(" Неверный логин или пароль!")
        return
    print(f"\n Добро пожаловать, {user['username']}! Ваша роль: {user['role']}")

    while True:
        if user['role'] == 'admin':
            menu_admin()
            choice = input("Выберите действие: ")
            if choice == '1':
                for p in get_all_patients(): print(p['last_name'], p['first_name'], '-', p['diagnosis'])
            elif choice == '2':
                ln = input("Фамилия: ")
                fn = input("Имя: ")
                d = input("Диагноз: ")
                add_patient(ln, fn, d)
                print("Добавлено!")
            elif choice == '3':
                pid = int(input("ID пациента: "))
                if delete_patient(pid): print("Удалено!")
            elif choice == '0':
                break

        elif user['role'] == 'user':
            menu_user()
            choice = input("Выберите действие: ")
            if choice == '1':
                for p in get_all_patients(): print(p['last_name'], p['first_name'], '-', p['diagnosis'])
            elif choice == '2':
                d = input("Диагноз: ")
                for p in search_patients_by_diagnosis(d): print(p['last_name'], p['first_name'], '-', p['diagnosis'])
            elif choice == '0':
                break
if __name__ == '__main__':
    main()
