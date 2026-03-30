from db.db_connect import Database
from datetime import datetime

class Complaints:
    def __init__(self, db=None):
        self.db = db or Database()

    def get_tenantID(self, apartmentnumber):
        apartment_query = "SELECT apartmentID FROM Apartment WHERE apartmentNumber = %s"
        apartment_row = self.db.fetch_one(apartment_query, (apartmentnumber,))
        if not apartment_row:
            return None

        lease_query = """
        SELECT tenantID
        FROM LeaseAgreement
        WHERE apartmentID = %s AND Status = 'active'
        """
        lease_row = self.db.fetch_one(lease_query, (apartment_row["apartmentID"],))
        if not lease_row:
            return None

        return lease_row["tenantID"]

    def add_complaint(self, reason, severity, apartmentnumber, complaintdetail):
        apartment_query = "SELECT apartmentID FROM Apartment WHERE apartmentNumber = %s"
        apartment_row = self.db.fetch_one(apartment_query, (apartmentnumber,))
        if not apartment_row:
            return False

        lease_query = """
        SELECT tenantID
        FROM LeaseAgreement
        WHERE apartmentID = %s AND Status = 'active'
        """
        lease_row = self.db.fetch_one(lease_query, (apartment_row["apartmentID"],))
        if not lease_row:
            return False

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """
        INSERT INTO Complaint (tenantID, apartmentID, InitialIssue, Description, reportDate, Severity, Status)
        VALUES (%s, %s, %s, %s, %s, %s, 'open')
        """

        self.db.execute(
            query,
            (
                lease_row["tenantID"],
                apartment_row["apartmentID"],
                (complaintdetail or "").strip(),
                (reason or "").strip(),
                timestamp,
                severity,
            ),
        )
        return True
