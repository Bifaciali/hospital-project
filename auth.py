from database import get_connection, hash_password

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    pwd_hash = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, pwd_hash)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)
    return None

def register_doctor(username, password, doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, doctor_id) VALUES (?, ?, 'user', ?)",
            (username, hash_password(password), doctor_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f" Ошибка регистрации: {e}")
        return False
    finally:
        conn.close()
