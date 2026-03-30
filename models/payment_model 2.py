from db.db import get_connection


def get_all_invoices():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.invoiceID, u.fullName, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    JOIN Tenant t ON l.tenantID = t.tenantID
    JOIN UserTbl u ON t.userID = u.userID
    ORDER BY i.dueDate DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def get_overdue_invoices():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.invoiceID, u.fullName, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    JOIN Tenant t ON l.tenantID = t.tenantID
    JOIN UserTbl u ON t.userID = u.userID
    WHERE i.Status = 'overdue'
    ORDER BY i.dueDate ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def mark_invoice_paid(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Invoice SET Status = 'paid' WHERE invoiceID = %s", (invoice_id,))
    conn.commit()
    conn.close()


def reset_invoice_status(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Invoice SET Status = 'pending' WHERE invoiceID = %s", (invoice_id,))
    conn.commit()
    conn.close()


def check_any_overdue():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Invoice WHERE Status = 'overdue'")
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0
