# admindashBE.py
from . import dbfunc
from . import user_session
import time, datetime

class adminBE():# values = ["All Roles", "Front-desk Staff", "Maintenance", "Finance"]
    def getStaffData():
        # tableColumns = ("ID", "Full Name", "Phone", "Email", "Role", "Location")
        conn = dbfunc.getconnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT u.userID, u.fullName, u.Phone, u.Email, u.Role, l.city
            FROM UserTbl u JOIN Location l ON u.locationID = l.locationID
            WHERE LOWER(u.Role) != 'tenant' ORDER BY u.Role ASC""")
        tableContents = cursor.fetchall()

        cursor.close()
        conn.close()

        return tableContents
    
    def getAptData(): 
        # tableColumns = ("Apartment", "City", "Tenant", "Lease Start", "Lease End", "Rent", "Status")
        conn = dbfunc.getconnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT a.apartmentNumber, t.fullName, u.Phone, u.Email, u.Role, l.city
            FROM UserTbl u JOIN Location l ON u.locationID = l.locationID
            WHERE LOWER(u.Role) != 'tenant' ORDER BY u.Role ASC""")
        tableContents = cursor.fetchall()

        cursor.close()
        conn.close()

        return tableContents

    def graph():
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        
        cursor.execute("""SELECT SUM(i.Amount + l.depositAmount - m.Cost) AS profit,
                    DATE_FORMAT(m.maintenanceDate, '%Y-%m') AS month 
                FROM MaintenanceLog m
                JOIN LeaseAgreement l ON m.apartmentID = l.apartmentID
                JOIN Apartment a On l.apartmentID = a.apartmentID
                JOIN Invoice i ON l.leaseID = i.leaseID
                WHERE i.Status = 'paid' AND a.locationID = %s
                GROUP BY month
                ORDER BY month ASC
                """, (user_session.user_base,))
        profitloss = cursor.fetchall()

        graphs = []
        for item in profitloss:
            graphs.append((item[1], item[0]))

        cursor.close()
        conn.close()

        return graphs
