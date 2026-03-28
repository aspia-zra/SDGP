import bcrypt
from db.db_connection import get_connection


class TenantTbl:

    @staticmethod
    def hash_password(password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()

    @staticmethod
    def login(email, password):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM Tenant WHERE Email = %s", (email,))
            tenant = cursor.fetchone()
            conn.close()

            if tenant is None:
                return None

            password_correct = bcrypt.checkpw(password.encode(), tenant["Password"].encode())

            if password_correct:
                return tenant
            else:
                return None

        except Exception as e:
            print("Tenant login error:", e)
            return None