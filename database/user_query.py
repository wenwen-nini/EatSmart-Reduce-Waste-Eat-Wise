from tkinter import messagebox as mb
from config.db_config import get_db

def login_user(username, password):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result:
        print("Login Successfully!")
        return result[0]
    else:
        print("Invalid username or password.")
        return None

def register_user(username, password, email):
    try:
        if (username == "" or password == "" or email == ""):
            mb.showerror("Register Failed!", "All fields are required.")
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email)
            )
            db.commit()
            cursor.close()
            db.close()
            mb.showinfo("Registration Success", "Registration Completed!")
    except Exception as e:
        print("Error during registration:", e)

def getUserById(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT username FROM users WHERE userID = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result[0] if result else None

def getEmailById(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT email FROM users WHERE userID = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result[0] if result else None