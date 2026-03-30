from db.dbconnect import get_connection
from datetime import date
import models.user_session as user_session

def get_payments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    user_id = user_session.current_user_id

    query = """
    SELECT i.invoiceID, i.Amount, i.dueDate, i.Status
    FROM Tenant t
    JOIN LeaseAgreement l ON t.tenantID = l.tenantID
    JOIN Invoice i ON l.leaseID = i.leaseID
    WHERE t.userID = %s
    ORDER BY i.dueDate DESC
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def get_payment_summary():
    conn = get_connection()
    cursor = conn.cursor()

    user_id = user_session.current_user_id

    query = """
    SELECT i.Status, COUNT(*)
    FROM Tenant t
    JOIN LeaseAgreement l ON t.tenantID = l.tenantID
    JOIN Invoice i ON l.leaseID = i.leaseID
    WHERE t.userID = %s
    GROUP BY i.Status
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def check_late_payment():
    conn = get_connection()
    cursor = conn.cursor()

    user_id = user_session.current_user_id

    query = """
    SELECT i.*
    FROM Tenant t
    JOIN LeaseAgreement l ON t.tenantID = l.tenantID
    JOIN Invoice i ON l.leaseID = i.leaseID
    WHERE t.userID = %s AND i.Status = 'overdue'
    """
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results


def calculate_late_fee(amount):
    return float(amount) * 0.10  # 10% late fee


def update_overdue_invoices():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Invoice
        SET Status='overdue'
        WHERE dueDate < CURDATE() AND Status != 'paid'
        """
    )

    cursor.execute(
        """
        UPDATE Invoice
        SET Status='pending'
        WHERE dueDate >= CURDATE() AND Status != 'paid'
        """
    )

    conn.commit()
    conn.close()


def pay_invoice(invoiceID):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Amount, dueDate, Status FROM Invoice WHERE invoiceID=%s",
        (invoiceID,)
    )
    result = cursor.fetchone()

    if not result:
        conn.close()
        return None, None

    amount, dueDate, status = result
    amount = float(amount)

    if status == "paid":
        conn.close()
        return amount, 0

    
    lateFee = 0
    if dueDate < date.today():
        lateFee = calculate_late_fee(amount)

    total = amount + lateFee

    cursor.execute(
        "UPDATE Invoice SET Status='paid' WHERE invoiceID=%s",
        (invoiceID,)
    )

    conn.commit()
    conn.close()

    return total, lateFee