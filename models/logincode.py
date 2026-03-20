import bcrypt
from db.dbconnect import Database
from models.usersession import user_sessions

class UserTbl:
    def __init__(self):
        self.dbfunc = Database()
        # Hashes a password using bcrypt before storing in the database
        @staticmethod
        def hash_password(password):
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            return hashed.decode()

        @staticmethod
        def login(email, password):
            try:
                conn = self.dbfunc.getconnection()
                cursor = conn.cursor(dictionary=True)

                cursor.execute("SELECT * FROM UserTbl WHERE Email = %s", (email,))
                user = cursor.fetchone()
                conn.close()

                if user is None:
                    return None

                password_correct = bcrypt.checkpw(password.encode(), user["Password"].encode())

                if password_correct:
                    user_sessions.user_sessions(user)
                    return user
                else:
                    return None

            except Exception as e:
                print("Login error:", e)
                return None
    
        def logout():
            user_sessions.logged_in = False
            user_sessions.current_user_id = None