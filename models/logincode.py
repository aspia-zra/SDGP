import bcrypt
from db import db
from . import user_session

class UserTbl:
    # Hashes a password using bcrypt before storing in the database
    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()

    @staticmethod
    def _verify_password(password, stored_password):
        if stored_password is None:
            return False, False

        # Normalize DB value to text safely.
        if isinstance(stored_password, bytes):
            try:
                stored_password = stored_password.decode()
            except Exception:
                return False, False
        elif not isinstance(stored_password, str):
            stored_password = str(stored_password)

        # If it looks like a bcrypt hash, verify with bcrypt.
        if stored_password.startswith("$2a$") or stored_password.startswith("$2b$") or stored_password.startswith("$2y$"):
            try:
                return bcrypt.checkpw(password.encode(), stored_password.encode()), False
            except Exception:
                return False, False

        # Backward-compatibility for old plaintext rows.
        return password == stored_password, True

    @staticmethod
    def login(email, password):
        conn = None
        cursor = None
        try:
            conn = db.getconnection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM UserTbl WHERE Email = %s", (email,))
            user = cursor.fetchone()

            if user is None:
                return None

            password_correct, was_plaintext = UserTbl._verify_password(password, user.get("Password"))

            if password_correct:
                if was_plaintext:
                    # Upgrade old plaintext password to bcrypt hash after successful login.
                    upgraded_hash = UserTbl.hash_password(password)
                    cursor.execute("UPDATE UserTbl SET Password = %s WHERE userID = %s", (upgraded_hash, user["userID"]))
                    conn.commit()
                    user["Password"] = upgraded_hash

                user_session.user_sessions(user)
                return user
            else:
                return None

        except Exception as e:
            print("Login error:", e)
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
    
    def logout():
        user_session.logged_in = False
        user_session.current_user_id = None