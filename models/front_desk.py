from db.dbconnect import Database
import re

class FrontDesk:
    def __init__(self):
        self.db = Database()

    # ---------------- CREATE ----------------
    def insert_tenant(self, name, phone, ni_number, email):
        cursor = self.db.cursor()
        query = "INSERT INTO tenant (fullname, phone, national_Insurance, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, phone, ni_number, email))
        self.db.commit()
        cursor.close()

    def register_tenant(self, name, phone, ni, email):
        if not name or not phone or not ni or not email:
            raise ValueError("All fields are required")

        if not self.is_valid_phone(phone):
            raise ValueError("Phone must be 11 digits starting with 0")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        self.insert_tenant(name, phone, ni, email)

    # ---------------- READ ----------------
    # front_desk.py
    def get_all_tenants(self):
        # call .cursor on the connection inside Database
        cursor = self.db.conn.cursor(dictionary=True) 
        query = "SELECT * FROM tenant"
        cursor.execute(query)
        tenants = cursor.fetchall()
        cursor.close()
        return tenants

    def get_tenant_by_id(self, tenant_id):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM tenant WHERE tenantID = %s", (tenant_id,))
        tenant = cursor.fetchone()
        cursor.close()
        return tenant

    # ---------------- UPDATE ----------------
    def update_user(self, tenant_id, name, phone, ni_number, email):
        cursor = self.db.cursor()
        query = """
        UPDATE tenant
        SET fullname = %s, phone = %s, national_Insurance = %s, email = %s 
        WHERE id = %s
        """
        cursor.execute(query, (name, phone, ni_number, email, tenant_id))
        self.db.commit()
        cursor.close()

    def assign_apartment(self, tenant_id, apartment_id):
        cursor = self.db.cursor()
        query = "UPDATE leaseagreement SET tenantID = %s WHERE apartmentID = %s"
        cursor.execute(query, (tenant_id, apartment_id))
        self.db.commit()
        cursor.close()

    # ---------------- DELETE ----------------
    def delete_user(self, tenant_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tenant WHERE tenantID = %s", (tenant_id))
        self.db.commit()
        cursor.close()

    # ---------------- VALIDATION ----------------
    def is_valid_phone(self, phone):
        return re.match(r"^0\d{10}$", phone) is not None
    
    # in front_desk.py
    def get_all_apartments(self):
        cursor = self.db.conn.cursor(dictionary=True)
        cursor.execute("SELECT apartmentNumber FROM apartment WHERE status='available'")
        apartments = [row['apartmentNumber'] for row in cursor.fetchall()]
        cursor.close()
        return apartments