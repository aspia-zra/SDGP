# admindashBE.py
from db import db
from . import user_session
import time, datetime
import plotly.graph_objects as go

class adminBE():# values = ["All Roles", "Front-desk Staff", "Maintenance", "Finance"]
    def getStaffData():
        # tableColumns = ("ID", "Full Name", "Phone", "Email", "Role", "Location")
        conn = db.getconnection()
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
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT a.apartmentNumber, l.City, u.fullName, la.startDate,
            la.endDate, a.monthlyRent, a.Status
            FROM Apartment a
            LEFT JOIN LeaseAgreement la ON la.apartmentID = a.apartmentID
            LEFT JOIN Tenant t ON t.tenantID = la.tenantID
            LEFT JOIN UserTbl u ON u.Email = t.Email
            JOIN Location l ON l.locationID = a.locationID
            ORDER BY a.apartmentNumber ASC""")
        tableContents = cursor.fetchall()

        cursor.close()
        conn.close()

        return tableContents
    
    def getAptList():
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT apartmentNumber
            FROM Apartment
            WHERE Status = 'Occupied'
            ORDER BY apartmentNumber ASC""")
        aptList = cursor.fetchall()

        cursor.close()
        conn.close()

        return aptList


    def graph():
        conn = db.getconnection()
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
    
    def tenantGraphs(apt):
        # late payment history per property graph - left
        conn = db.getconnection()

        try:
            cursor = conn.cursor()
            cursor.execute(""" SELECT u.fullName, DATE_FORMAT(i.dueDate, '%Y-%m') AS month, 
                SUM(i.amount + l.depositAmount) AS paid
                FROM UserTbl u
                JOIN Tenant t ON t.Email = u.Email
                JOIN LeaseAgreement l ON l.tenantID = t.tenantID
                JOIN Apartment a ON a.apartmentID = l.apartmentID
                JOIN Invoice i ON i.leaseID = l.leaseID
                WHERE i.Status = 'paid' AND a.apartmentNumber = %s
                GROUP BY u.fullName, month""",(apt,))
            tenantData = cursor.fetchall()

            cursor.execute("SELECT apartmentID FROM Apartment WHERE apartmentNumber = %s"
                ,(apt,))
            result = cursor.fetchone()
            if result is None:
                return [], [], []
            apartmentID = result[0]

            if apartmentID >= 1:
                cursor.execute("SELECT COUNT(*) FROM Apartment WHERE apartmentID = %s", (apartmentID-1,))
                prevExists = cursor.fetchone()[0] > 0

                if prevExists:
                    cursor.execute(""" SELECT u.fullName, DATE_FORMAT(i.dueDate, '%Y-%m') AS month, 
                    SUM(i.amount + l.depositAmount) AS paid
                    FROM UserTbl u
                    JOIN Tenant t ON t.Email = u.Email
                    JOIN LeaseAgreement l ON l.tenantID = t.tenantID
                    JOIN Invoice i ON i.leaseID = l.leaseID
                    WHERE i.Status = 'paid' AND l.apartmentID = %s
                    GROUP BY u.fullName, month""",(apartmentID-1,))
                    neighbour1 = cursor.fetchall()
                else:
                    neighbour1 = None

                cursor.execute("SELECT COUNT(*) FROM Apartment WHERE apartmentID = %s", (apartmentID+1,))
                nextExists = cursor.fetchone()[0] > 0
                
                if nextExists:
                    cursor.execute(""" SELECT u.fullName, DATE_FORMAT(i.dueDate, '%Y-%m') AS month, 
                    SUM(i.amount + l.depositAmount) AS paid
                    FROM UserTbl u
                    JOIN Tenant t ON t.Email = u.Email
                    JOIN LeaseAgreement l ON l.tenantID = t.tenantID
                    JOIN Invoice i ON i.leaseID = l.leaseID
                    WHERE i.Status = 'paid' AND l.apartmentID = %s
                    GROUP BY u.fullName, month""",(apartmentID+1,))
                    neighbour2 = cursor.fetchall()
                else: 
                    neighbour2 = None

                return tenantData, neighbour1, neighbour2
            else:
                cursor.execute("SELECT COUNT(*) FROM Apartment WHERE apartmentID = %s", (apartmentID+1,))
                nextExists = cursor.fetchone()[0] > 0

                if nextExists:
                    cursor.execute(""" SELECT u.fullName, DATE_FORMAT(i.dueDate, '%Y-%m') AS month, 
                    SUM(i.amount + l.depositAmount) AS paid
                    FROM UserTbl u
                    JOIN Tenant t ON t.Email = u.Email
                    JOIN LeaseAgreement l ON l.tenantID = t.tenantID
                    JOIN Invoice i ON i.leaseID = l.leaseID
                    WHERE i.Status = 'paid' AND l.apartmentID = %s
                    GROUP BY u.fullName, month""",(apartmentID+1,))
                    neighbour1 = cursor.fetchall()
                else:
                    neighbour1 = None

                return tenantData, neighbour1, None
        finally:
            cursor.close()
            conn.close()
        
