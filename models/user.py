import bcrypt
from db.db import get_connection


class UserTbl:

    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()

    @staticmethod
    def login(email, password):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM UserTbl WHERE Email = %s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user is None:
                return None

            password_correct = bcrypt.checkpw(password.encode(), user["Password"].encode())

            if password_correct:
                return user
            else:
                return None

        except Exception as e:
            print("Login error:", e)
            return None