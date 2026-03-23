from db.db_connect import Database
from datetime import datetime
from tkinter.ttk import Button, Entry
import tkinter.messagebox as messagebox

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

    def submit_complaint(self):
        reason = self.Entrycomplaint.get()
        severity = self.Entryseverity.get()
        apartmentnumber = self.Entryapartmentnumber.get()
        complaintdetail = self.Entrycomplaintdetail.get()

        inserted = self.add_complaint(reason, severity, apartmentnumber, complaintdetail)
        if (inserted == True):
            messagebox.showinfo("Success", "Complaint submitted successfully")
            self.get_complaint_history() #refreshes the table that shows 5 most recent complaints

    def get_recent_complaints(self, tenantID):
        query = """
        SELECT Description, reportDate, Severity, Status
        FROM Complaint
        WHERE tenantID = %s
        ORDER BY reportDate DESC
        LIMIT 5
        """
        return self.db.fetch_all(query, (tenantID,))
    
    def get_complaint_history(self):
        tenantID = self.get_tenantID(self.Entryapartmentnumber.get())
        complaints = self.get_recent_complaints(tenantID)

        # Clear existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data into the treeview
        for complaint in complaints:
            reason = complaint["Description"]
            timestamp = complaint["reportDate"]
            severity = complaint["Severity"]
            status = complaint["Status"]
            self.tree.insert("", "end", values=(reason, timestamp, severity, status))
