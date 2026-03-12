# admindashBE.py
from . import dbfunc
from . import user_session
import time, datetime

def progressbarCalc():
    conn = dbfunc.getconnection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Apartment WHERE locationID=%s"
        ,(user_session.user_base,))
    totalApt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Apartment WHERE Status='occupied' " \
        "AND locationID=%s", (user_session.user_base,))
    aptOccupied = cursor.fetchone()[0] 
    aptPercent = (aptOccupied/totalApt)*100 if totalApt else 0

    cursor.execute("""SELECT COUNT(*) FROM Invoice i
        JOIN LeaseAgreement l ON i.leaseID = l.leaseID
        JOIN Apartment a ON l.apartmentID = a.apartmentID
        WHERE a.locationID=%s""" ,(user_session.user_base,))
    totalInvoice = cursor.fetchone()[0] 
    cursor.execute("""SELECT COUNT(*) FROM Invoice i
        JOIN LeaseAgreement l ON i.leaseID = l.leaseID
        JOIN Apartment a ON l.apartmentID = a.apartmentID
        WHERE i.Status='paid' AND a.locationID=%s""", (user_session.user_base,))
    invoicePaid = cursor.fetchone()[0]
    invoicePercent = (invoicePaid/totalInvoice)*100 if totalInvoice else 0

    cursor.execute("""SELECT COUNT(*) FROM Complaint c
        JOIN Apartment a ON c.apartmentID = a.apartmentID
        WHERE a.locationID=%s""" ,(user_session.user_base,))
    totalComp = cursor.fetchone()[0]
    cursor.execute("""SELECT COUNT(*) FROM Complaint c
        JOIN Apartment a ON c.apartmentID = a.apartmentID
        WHERE c.Status='closed' AND a.locationID=%s""", (user_session.user_base,))
    compResolved = cursor.fetchone()[0]
    compPercent = (compResolved/totalComp)*100 if totalComp else 0

    cursor.close()
    conn.close()

    return aptPercent, invoicePercent, compPercent

def dropdownBoxes():
    conn = dbfunc.getconnection()
    cursor = conn.cursor()
    cursor.execute("""SELECT l.endDate, u.fullName
        FROM LeaseAgreement l
        JOIN Tenant t ON l.tenantID = t.tenantID
        JOIN UserTbl u ON t.userID = u.userID
        JOIN Apartment a ON l.apartmentID = a.apartmentID
        WHERE l.endDate >= CURDATE() AND a.locationID=%s
        ORDER BY l.endDate ASC
        LIMIT 3""",(user_session.user_base, ))
    leases = cursor.fetchall()

    # Overdue rent
    cursor.execute("""SELECT i.Amount, i.dueDate, u.fullName
        FROM Invoice i
        JOIN LeaseAgreement l ON i.leaseID = l.leaseID
        Join tenant t ON l.tenantID = t.tenantID
        Join UserTbl u ON t.userID = u.userID
        JOIN Apartment a ON l.apartmentID = a.apartmentID
        WHERE i.dueDate <= CURDATE() AND i.Status = 'overdue' 
            AND a.locationID=%s
        ORDER BY i.dueDate ASC
        LIMIT 3""",(user_session.user_base, ))
    overdues = cursor.fetchall()

    # High Priority Repairs
    cursor.execute("""SELECT c.Severity, c.Description, u.fullName
        FROM Complaint c
        Join tenant t ON c.tenantID = t.tenantID
        Join UserTbl u ON t.userID = u.userID
        JOIN Apartment a ON c.apartmentID = a.apartmentID           
        WHERE c.Status = 'open' AND a.locationID=%s
        ORDER BY c.Severity DESC
        LIMIT 3""",(user_session.user_base, ))
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

    return graphs
