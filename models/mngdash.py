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
                            l.City,
                            a.monthlyRent,
                            a.Status,
                            lease.endDate
                        FROM Apartment a
                        JOIN Location l
                            ON a.locationID = l.locationID
                        LEFT JOIN LeaseAgreement lease
                            ON a.apartmentID = lease.apartmentID
                        ORDER BY a.apartmentNumber
                     """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data # back to FE table
    
    