# admindashBE.py
from db import db
# from . import user_session
# import time, datetime

class mngBE():# values = ["All Roles", "Front-desk Staff", "Maintenance", "Finance"]
    @staticmethod
    def getAptData(): 
        # tableColumns = ("Apartment", "City", "Tenant", "Lease Start", "Lease End", "Rent", "Status")
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT 
                            a.apartmentNumber, 
                            a.locationID, 
                            lease.monthlyRent, 
                            lease.Status, 
                            lease.endDate
                        FROM apartment, a
                        JOIN leaseagreement lease
                            ON a.apartmentID = lease.apartmentID
                     """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data # back to FE table
    
    