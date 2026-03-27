from .. import dbfunc

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
                WHERE l.City = %s
                GROUP BY a.apartmentID, a.apartmentNumber,
                         a.Type, a.monthlyRent,
                         a.Status, l.City
            ''')
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
                GROUP BY a.apartmentID, a.apartmentNumber,
                         a.Type, a.monthlyRent,
                         a.Status, l.City''')
            
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
            ORDER BY i.dueDate DESC''')
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
            ORDER BY ml.maintenanceDate DESC''')
        result = cursor.fetchall()

        cursor.close()
        conn.close

        return result