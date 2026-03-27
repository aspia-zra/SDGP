from .. import dbfunc, user_session

class ReportModel:
    @staticmethod
    def get_financial_report():
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.invoiceID, i.Amount, i.dueDate,
                   i.Status, u.fullName
            FROM Invoice i
            JOIN LeaseAgreement ls
                ON i.leaseID = ls.leaseID
            JOIN Tenant t
                ON ls.tenantID = t.tenantID
            JOIN UserTbl u
                ON t.userID = u.userID
            WHERE u.locationID = %s
            ORDER BY i.dueDate DESC''', (user_session.user_base,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result