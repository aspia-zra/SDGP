from db.db_connection import get_connection
from datetime import date
import models.user_session as user_session

LATE_FEE = 25


# ================= GET PAYMENTS (FILTERED BY LOGGED-IN USER) =================
def get_payments():
    conn = get_connection()
    cursor = conn.cursor()

    user_id = user_session.current_user_id
    print("USER ID IN BACKEND:", user_session.current_user_id)

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


# ================= PAYMENT SUMMARY (PER USER) =================
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


# ================= CHECK LATE PAYMENTS (PER USER) =================
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


# ================= CALCULATE LATE FEE =================
def calculate_late_fee(amount):
    return float(amount) * 0.10  # 10% late fee


# ================= PAY INVOICE =================
def pay_invoice(invoiceID):
    conn = get_connection()
    cursor = conn.cursor()

    # Get invoice details
    cursor.execute(
        "SELECT Amount, dueDate FROM Invoice WHERE invoiceID=%s",
        (invoiceID,)
    )

    result = cursor.fetchone()

    if not result:
        conn.close()
        return None, None

    amount, dueDate = result

    lateFee = 0

    # Apply late fee if overdue
    if dueDate < date.today():
        lateFee = LATE_FEE

    total = amount + lateFee

    # Insert payment record
    cursor.execute(
        """
        INSERT INTO payments(invoiceID, amountPaid, paymentDate, lateFee)
        VALUES (%s, %s, CURDATE(), %s)
        """,
        (invoiceID, total, lateFee)
    )

    # Update invoice status
    cursor.execute(
        "UPDATE Invoice SET Status='paid' WHERE invoiceID=%s",
        (invoiceID,)
    )

    conn.commit()
    conn.close()

    return total, lateFee