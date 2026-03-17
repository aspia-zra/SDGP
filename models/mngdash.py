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

        cursor.execute("""SELECT a.apartmentNumber, l.city
            FROM UserTbl u JOIN Location l ON u.locationID = l.locationID
            WHERE LOWER(u.Role) != 'tenant' ORDER BY u.Role ASC""")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data
    
    