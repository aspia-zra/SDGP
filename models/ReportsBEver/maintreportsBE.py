from . import dbfunc, user_session

class ReportModel:
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