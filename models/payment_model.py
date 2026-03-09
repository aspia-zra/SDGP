from db.db_connection import get_connection


def get_tenant_payments(tenant_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT i.invoiceID, i.Amount, i.dueDate, i.Status
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    WHERE l.tenantID = %s
    """

    cursor.execute(query, (tenant_id,))
    data = cursor.fetchall()

    conn.close()
    return data


def get_payment_summary(tenant_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT i.Status, COUNT(*)
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    WHERE l.tenantID = %s
    GROUP BY i.Status
    """

    cursor.execute(query, (tenant_id,))
    data = cursor.fetchall()

    conn.close()
    return data


def check_late_payment(tenant_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM Invoice i
    JOIN LeaseAgreement l ON i.leaseID = l.leaseID
    WHERE l.tenantID = %s
    AND i.Status = 'overdue'
    """

    cursor.execute(query, (tenant_id,))
    result = cursor.fetchone()[0]

    conn.close()

    return result > 0


def pay_invoice(invoice_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE Invoice
    SET Status = 'paid'
    WHERE invoiceID = %s
    """

    cursor.execute(query, (invoice_id,))
    conn.commit()

    conn.close()