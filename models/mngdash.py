# admindashBE.py
from db import db
# from . import user_session
# import time, datetime

class adminBE():# values = ["All Roles", "Front-desk Staff", "Maintenance", "Finance"]
    
    def getAptData(): 
        # tableColumns = ("Apartment", "City", "Tenant", "Lease Start", "Lease End", "Rent", "Status")
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT a.apartmentNumber, t.fullName, u.Phone, u.Email, u.Role, l.city
            FROM UserTbl u JOIN Location l ON u.locationID = l.locationID
            WHERE LOWER(u.Role) != 'tenant' ORDER BY u.Role ASC""")
        tableContents = cursor.fetchall()

        cursor.close()
        conn.close()

        return tableContents
    
    