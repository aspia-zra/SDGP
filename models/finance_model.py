from db import db as dbfunc
from . import user_session

class FinanceModel:

    @staticmethod
    def get_summary():
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                COUNT(*),
                SUM(CASE WHEN i.Status="pending"
                    THEN Amount ELSE 0 END),
                SUM(CASE WHEN i.Status="overdue"
                    THEN Amount ELSE 0 END),
                SUM(CASE WHEN i.Status="paid"
                    THEN Amount ELSE 0 END),
                COUNT(CASE WHEN i.Status="pending" THEN 1 END),
                COUNT(CASE WHEN i.Status="overdue" THEN 1 END),
                COUNT(CASE WHEN i.Status="paid"    THEN 1 END)
            FROM Invoice i JOIN LeaseAgreement la ON la.leaseID = i.leaseID
            JOIN Apartment a ON la.apartmentID = a.apartmentID
            WHERE a.locationID = %s''', (user_session.user_base,))
        return cursor.fetchone()

    @staticmethod
    def get_recent_transactions(limit=10):
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   i.Status, u.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls
                ON i.leaseID = ls.leaseID
            JOIN Tenant t
                ON ls.tenantID = t.tenantID
            JOIN UserTbl u
                ON t.userID = u.userID
            JOIN Apartment a
                ON ls.apartmentID = a.apartmentID
            WHERE a.locationID = %s
            ORDER BY i.Created_at DESC
            LIMIT %s
        ''', (user_session.user_base, limit))
        return cursor.fetchall()

    @staticmethod
    def get_upcoming_dues():
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   u.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls
                ON i.leaseID = ls.leaseID
            JOIN Tenant t
                ON ls.tenantID = t.tenantID
            JOIN UserTbl u
                ON t.userID = u.userID
            JOIN Apartment a
                ON ls.apartmentID = a.apartmentID
            WHERE i.Status IN ("pending", "overdue") AND a.locationID=%s
            ORDER BY i.dueDate ASC
            LIMIT 10''', (user_session.user_base,))
        return cursor.fetchall()
