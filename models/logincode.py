from db.dbconnect import *
import models.user_session as user_sessions
import bcrypt

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
                user_sessions(user)
                return user
            else:
                return None

        except Exception as e:
            print("Login error:", e)
            return None

    @staticmethod
    def logout():
        user_sessions.logged_in = False
        user_sessions.current_user_id = None
        user_sessions.current_user_name = ""
        user_sessions.current_email = ""
        user_sessions.current_phone = ""
        user_sessions.user_type = ""
        user_sessions.user_base = None
        user_sessions.personal_fontsize = 12