from db.dbconnect import *
import re

class FrontDesk:

    def insert_tenant(self, name, phone, ni_number, email):
        conn = get_connection()
        cursor = conn.cursor()
        role = 'tenant'
        password = 'password'

        query = "INSERT INTO usertbl (fullName, Phone, Email, Role, Password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, phone, email, role, password))
        conn.commit()
        cursor.close()

        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO tenant (national_Insurance, Email) VALUES (%s, %s)"
        cursor.execute(query, (ni_number, email))
        conn.commit()
        cursor.close()


    def register_tenant(self, name, phone, ni, email):
        if not name or not phone or not ni or not email:
            raise ValueError("All fields are required")

        if not self.is_valid_phone(phone):
            raise ValueError("Phone must be 11 digits starting with 0")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        self.insert_tenant(name, phone, ni, email)

    def get_all_tenants(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 
        query = ("""SELECT t.tenantID, u.fullName, u.Phone, t.national_Insurance, t.Email, u.Created_at, t.status 
            FROM Tenant t JOIN UserTbl u ON t.userID = u.userID""")
        cursor.execute(query)
        tenants = cursor.fetchall()
        cursor.close()
        return tenants

    def get_tenant_by_id(self, tenant_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tenant WHERE t.tenantID=%s""", (tenant_id,))
        tenant = cursor.fetchone()
        cursor.close()
        return tenant

    def update_user(self, tenant_id, name, phone, ni_number, email):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE tenant
        SET fullname = %s, phone = %s, national_Insurance = %s, email = %s 
        WHERE id = %s
        """
        cursor.execute(query, (name, phone, ni_number, email, tenant_id))
        conn.commit()
        cursor.close()

    def assign_apartment(self, tenant_id, apartment_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE leaseagreement SET tenantID = %s WHERE apartmentID = %s"
        cursor.execute(query, (tenant_id, apartment_id))
        conn.commit()
        cursor.close()

    def delete_user(self, tenant_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tenant WHERE tenantID = %s", (tenant_id))
        conn.commit()
        cursor.close()

    def is_valid_phone(self, phone):
        return re.match(r"^0\d{10}$", phone) is not None
    
    def get_all_apartments(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT apartmentID FROM apartment WHERE status='available'")
        apartments = [row['apartmentID'] for row in cursor.fetchall()]
        cursor.close()
        return apartments