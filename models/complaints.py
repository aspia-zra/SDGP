from db.dbconnect import *
from datetime import datetime
from tkinter.ttk import Button, Entry
import tkinter.messagebox as messagebox

class Complaints:
    def get_tenantID(self, apartmentnumber):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)


        cursor.execute("SELECT apartmentID FROM apartment WHERE apartmentNumber = %s", (apartmentnumber,))
        apartmentID = cursor.fetchone()
        apartmentID = apartmentID['apartmentID']

        cursor.execute("SELECT tenantID FROM leaseagreement WHERE apartmentID = %s AND Status = 'active'", (apartmentID,))
        tenantID = cursor.fetchone()
        tenantID = tenantID['tenantID']

        conn.close()
        return tenantID

    def add_complaint(self, reason, severity, apartmentnumber, complaintdetail, tenantID):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT apartmentID FROM apartment WHERE apartmentNumber = %s", (apartmentnumber,))
        apartmentID = cursor.fetchone()
        apartmentID = apartmentID['apartmentID']

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = "INSERT INTO complaint (tenantID, apartmentID, Initial_Issue, Description, ReportDate, severity) VALUES (%s, %s, %s,%s, %s, %s)"

        cursor.execute(query, (tenantID, apartmentID, reason,complaintdetail, timestamp, severity))
        conn.commit()
        conn.close()
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
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT Description, timestamp, severity, status FROM complaint WHERE tenantID = %s ORDER BY timestamp DESC LIMIT 5"
        cursor.execute(query, (tenantID,))
        complaints = cursor.fetchall()

        conn.close()
        return complaints
    
    # def get_complaint_history(self):
    #     tenantID = self.get_tenantID(self.Entryapartmentnumber.get())
    #     complaints = self.get_recent_complaints(tenantID)

    #     # Clear existing data in the treeview
    #     for item in self.tree.get_children():
    #         self.tree.delete(item)

    #     # Insert new data into the treeview
    #     for complaint in complaints:
    #         reason, timestamp, severity, status = complaint
    #         self.tree.insert("", "end", values=(reason, timestamp, severity, status))