import bcrypt
from . import dbfunc 
from . import user_session

class UserTbl:
    # Hashes a password using bcrypt before storing in the database
    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()

    @staticmethod
    def login(email, password):
        try:
            conn = dbfunc.getconnection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM UserTbl WHERE Email = %s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user is None:
                return None

            password_correct = bcrypt.checkpw(password.encode(), user["Password"].encode())

            if password_correct:
                user_session.user_sessions(user)
                return user
            else:
                return None

        except Exception as e:
            print("Login error:", e)
            return None
    
    def logout():
        user_session.logged_in = False
        user_session.current_user_id = None