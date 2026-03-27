from .. import dbfunc, user_session

class ReportModel:
    @staticmethod
    def get_occupancy_report(city=None):
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        if city:
            cursor.execute('''
                SELECT a.apartmentNumber, a.Type,
                       a.monthlyRent, a.Status, l.City,
                       COUNT(ls.leaseID) AS num_tenants
                FROM Apartment a
                JOIN Location l ON a.locationID = l.locationID
                LEFT JOIN LeaseAgreement ls
                    ON a.apartmentID = ls.apartmentID
                    AND ls.Status = "active"
                WHERE l.City = %s AND l.locationID = %s
                GROUP BY a.apartmentID, a.apartmentNumber,
                         a.Type, a.monthlyRent,
                         a.Status, l.City
            ''', (city,user_session.user_base))
        else:
            cursor.execute('''
                SELECT a.apartmentNumber, a.Type,
                       a.monthlyRent, a.Status, l.City,
                       COUNT(ls.leaseID) AS num_tenants
                FROM Apartment a
                JOIN Location l
                    ON a.locationID = l.locationID
                LEFT JOIN LeaseAgreement ls
                    ON a.apartmentID = ls.apartmentID
                    AND ls.Status = "active"
                WHERE l.locationID = %s
                GROUP BY a.apartmentID, a.apartmentNumber,
                         a.Type, a.monthlyRent,
                         a.Status, l.City''', (user_session.user_base,))
            
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return result

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

    @staticmethod
    def get_maintenance_report():
        conn = dbfunc.getconnection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ml.logID, a.apartmentNumber,
                   ml.maintenanceDate, ml.timeTaken,
                   ml.Cost, COALESCE(ml.RepairDetails, "")
            FROM MaintenanceLog ml
            JOIN Apartment a
                ON ml.apartmentID = a.apartmentID
            WHERE a.locationID = %s
            ORDER BY ml.maintenanceDate DESC''', (user_session.user_base,))
        result = cursor.fetchall()

        cursor.close()
        conn.close

        return result