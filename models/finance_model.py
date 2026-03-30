from db.db import get_connection


class FinanceModel:

    @staticmethod
    def get_summary():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                COUNT(*),
                SUM(CASE WHEN Status="pending" THEN Amount ELSE 0 END),
                SUM(CASE WHEN Status="overdue" THEN Amount ELSE 0 END),
                SUM(CASE WHEN Status="paid" THEN Amount ELSE 0 END),
                COUNT(CASE WHEN Status="pending" THEN 1 END),
                COUNT(CASE WHEN Status="overdue" THEN 1 END),
                COUNT(CASE WHEN Status="paid" THEN 1 END)
            FROM Invoice
        ''')
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_recent_transactions(limit=10):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   i.Status, u.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls ON i.leaseID = ls.leaseID
            JOIN Tenant t ON ls.tenantID = t.tenantID
            JOIN UserTbl u ON t.userID = u.userID
            JOIN Apartment a ON ls.apartmentID = a.apartmentID
            ORDER BY i.Created_at DESC
            LIMIT %s
        ''', (limit,))
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_upcoming_dues():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   u.fullName, a.apartmentNumber
            FROM Invoice i
            JOIN LeaseAgreement ls ON i.leaseID = ls.leaseID
            JOIN Tenant t ON ls.tenantID = t.tenantID
            JOIN UserTbl u ON t.userID = u.userID
            JOIN Apartment a ON ls.apartmentID = a.apartmentID
            WHERE i.Status IN ("pending", "overdue")
            ORDER BY i.dueDate ASC
            LIMIT 10
        ''')
        result = cursor.fetchall()
        conn.close()
        return result