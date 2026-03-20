from db.dbconnect import Database
from datetime import datetime
from tkinter.ttk import Button, Entry
import tkinter.messagebox as messagebox

class Complaints:
    def __init__(self):
        self.db = Database()

    def get_tenantID(self, apartmentnumber):

        cursor = self.db.cursor
        conn = self.db.conn


        cursor.execute("SELECT apartmentID FROM apartments WHERE apartmentnumber = %s", (apartmentnumber,))
        apartmentID = cursor.fetchone()
        apartmentID = apartmentID['apartmentID']

        cursor.execute("SELECT tenantID FROM leaseagreement WHERE apartmentID = %s AND Status = 'active'", (apartmentID,))
        tenantID = cursor.fetchone()
        tenantID = tenantID['tenantID']

        conn.close()
        return tenantID

    def add_complaint(self, reason, severity, apartmentnumber, complaintdetail):
        cursor = self.db.cursor
        conn = self.db.conn


        #collect apartment ID from apartment number to insert into complaints table
        cursor.execute("SELECT apartmentID FROM apartments WHERE apartmentnumber = %s", (apartmentnumber,))
        apartmentID = cursor.fetchone()
        apartmentID = apartmentID['apartmentID']

        #collect tenantID from leaseagreement table using apartmentID for the complaints table
        cursor.execute("SELECT tenantID FROM leaseagreement WHERE apartmentID = %s AND Status = 'active'", (apartmentID,))
        tenantID = cursor.fetchone()
        tenantID = tenantID['tenantID']

        #add all the information collected into the complaints table

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = "INSERT INTO complaints (tenantID, apartmentID, complaintdetail, reason, timestamp, severity) VALUES (%s, %s, %s,%s, %s, %s)"

        cursor.execute(query, (tenantID, apartmentID, complaintdetail, reason, timestamp, severity))
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
        cursor = self.db.cursor
        conn = self.db.conn


        query = "SELECT reason, timestamp, severity, status FROM complaints WHERE tenantID = %s ORDER BY timestamp DESC LIMIT 5"
        cursor.execute(query, (tenantID,))
        complaints = cursor.fetchall()

        conn.close()
        return complaints
    
    def get_complaint_history(self):
        tenantID = self.get_tenantID(self.Entryapartmentnumber.get())
        complaints = self.get_recent_complaints(tenantID)

        # Clear existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data into the treeview
        for complaint in complaints:
            reason, timestamp, severity, status = complaint
            self.tree.insert("", "end", values=(reason, timestamp, severity, status))