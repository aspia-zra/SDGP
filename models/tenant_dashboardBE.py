from db.dbconnect import get_connection
import models.user_session as user_session


def get_tenant_data():
    conn = get_connection()
    if conn is None:
        return {}

    cursor = conn.cursor(dictionary=True)

    user_id = user_session.current_user_id

    query = """
    SELECT 
        u.fullName,
        u.Email,
        u.Phone,
        t.national_Insurance,
        t.Status AS tenantStatus,

        a.apartmentNumber,
        a.Type,
        a.monthlyRent,
        a.Status AS apartmentStatus,

        l.Address,
        l.City,
        l.Phone AS locationPhone,

        la.startDate,
        la.endDate,
        la.depositAmount,
        la.Status AS leaseStatus

    FROM usertbl u
    JOIN tenant t ON u.userID = t.userID
    JOIN leaseagreement la ON t.tenantID = la.tenantID
    JOIN apartment a ON la.apartmentID = a.apartmentID
    JOIN location l ON a.locationID = l.locationID

    WHERE u.userID = %s
    """

    try:
        cursor.execute(query, (user_id,))
        data = cursor.fetchone()
        return data or {}
    finally:
        cursor.close()
        conn.close()