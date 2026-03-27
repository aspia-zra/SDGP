# admindashBE.py
from db import db
from . import user_session
import time, datetime
import bcrypt

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
    
    def addStaff(fullname,phone,email,password,role):
        conn = db.getconnection()
        cursor = conn.cursor()

        today = datetime.datetime.now().date()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute("""INSERT INTO UserTbl (fullName, Phone, Email, Password,
            Role, locationID, Created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (fullname, phone, email, hashed, role, user_session.user_base, today))
        conn.commit()

        cursor.close()
        conn.close()

    def editStaff(userId, fullname, phone, email, role): ##COMPLETE
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""UPDATE UserTbl 
            SET fullName = %s , Phone = %s, Email = %s, Role = %s
            WHERE userID = %s""",(fullname, phone, email, role, userId))
        conn.commit()

        cursor.close()
        conn.close()
    
    def getAptData(): 
        # tableColumns = ("Apartment", "City", "Tenant", "Lease Start", "Lease End", "Rent", "Status")
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT a.apartmentNumber, l.City, u.fullName, la.startDate,
            la.endDate, a.monthlyRent, a.Status
            FROM Apartment a
            LEFT JOIN LeaseAgreement la ON la.apartmentID = a.apartmentID
            LEFT JOIN Tenant t ON t.tenantID = la.tenantID
            LEFT JOIN UserTbl u ON u.userID = t.userID
            JOIN Location l ON l.locationID = a.locationID
            ORDER BY 
                CASE 
                    WHEN la.endDate IS NULL THEN 1 
                    ELSE 0 
                END,
                la.endDate ASC""")
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
        cursor = None

        try:
            cursor = conn.cursor()
            cursor.execute(""" SELECT u.fullName, DATE_FORMAT(i.dueDate, '%Y-%m') AS month, 
                SUM(i.amount + l.depositAmount) AS paid
                FROM Tenant t
                JOIN UserTbl u ON u.userID = t.userID
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
                    FROM Tenant t
                    JOIN UserTbl u ON u.userID = t.userID
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
                    FROM Tenant t
                    JOIN UserTbl u ON u.userID = t.userID
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
                    FROM Tenant t
                    JOIN UserTbl u ON u.userID = t.userID
                    JOIN LeaseAgreement l ON l.tenantID = t.tenantID
                    JOIN Invoice i ON i.leaseID = l.leaseID
                    WHERE i.Status = 'paid' AND l.apartmentID = %s
                    GROUP BY u.fullName, month""",(apartmentID+1,))
                    neighbour1 = cursor.fetchall()
                else:
                    neighbour1 = None

                return tenantData, neighbour1, None
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
        