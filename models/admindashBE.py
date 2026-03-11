# admindashBE.py
from . import dbfunc
import time, datetime

def progressbarCalc():
    conn = dbfunc.getconnection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Apartment")
    totalApt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Apartment WHERE Status='occupied'")
    aptOccupied = cursor.fetchone()[0]
    aptPercent = (aptOccupied/totalApt)*100

    cursor.execute("SELECT COUNT(*) FROM Invoice")
    totalInvoice = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Invoice WHERE Status='paid'")
    invoicePaid = cursor.fetchone()[0]
    invoicePercent = (invoicePaid/totalInvoice)*100

    cursor.execute("SELECT COUNT(*) FROM Complaint")
    totalComp = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Complaint WHERE Status='closed'")
    compResolved = cursor.fetchone()[0]
    compPercent = (compResolved/totalComp)*100

    cursor.close()
    conn.close()

    return aptPercent, invoicePercent, compPercent

def dropdownBoxes():
    conn = dbfunc.getconnection()
    cursor = conn.cursor()
    cursor.execute("""SELECT l.endDate, u.fullName
        FROM LeaseAgreement l
        JOIN Tenant t ON l.tenantID = t.tenantID
        Join UserTbl u ON t.userID = u.userID
        WHERE l.endDate >= CURDATE()
        ORDER BY l.endDate ASC
        LIMIT 3""")
    leases = cursor.fetchall()

    # Overdue rent
    cursor.execute("""SELECT i.Amount, i.dueDate, u.fullName
        FROM Invoice i
        JOIN LeaseAgreement l ON i.leaseID = l.leaseID
        Join tenant t ON l.tenantID = t.tenantID
        Join UserTbl u ON t.userID = u.userID
        WHERE i.dueDate <= CURDATE() AND i.Status = 'overdue'
        ORDER BY i.dueDate ASC
        LIMIT 3""")
    overdues = cursor.fetchall()

    # High Priority Repairs
    cursor.execute("""SELECT c.Severity, m.Cost, u.fullName
        FROM Complaint c
        Join tenant t ON c.tenantID = t.tenantID
        Join UserTbl u ON t.userID = u.userID
        Join MaintenanceLog m ON c.complaintID = m.complaintID
        WHERE c.Status = 'open'
        ORDER BY c.Severity DESC
        LIMIT 3""")
    repairs = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return leases, overdues, repairs


def graph():
    conn = dbfunc.getconnection()
    cursor = conn.cursor()
    
    cursor.execute("""SELECT SUM(i.Amount + l.depositAmount - m.Cost) AS profit,
                   DATE_FORMAT(m.maintenanceDate, '%Y-%m') AS month 
            FROM MaintenanceLog m
            JOIN LeaseAgreement l ON m.apartmentID = l.apartmentID
            JOIN Invoice i ON l.leaseID = i.leaseID
            WHERE i.Status = 'paid'
            GROUP BY month
            ORDER BY month ASC
            """)
    profitloss = cursor.fetchall()

    graphs = []
    for item in profitloss:
        graphs.append((item[1], item[0]))

    return graphs
