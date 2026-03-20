import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db.dbconnect import Database
from models.complaints import Complaints
import gui.navbar as nav
from gui.theme import *

class ComplaintsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND)

        self.controller = controller
        self.models = Complaints()

        self.db = Database()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_form()

        self.nav = nav.navbar(self, parent)
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

    def submit_complaint(self):
        reason = self.Entrycomplaint.get()
        severity = self.severity.get()
        apartmentnumber = self.EntryAPID.get()
        complaintdetail = self.EntryComplaintDetails.get("1.0", "end")
        
        inserted = self.models.add_complaint(reason, severity, apartmentnumber, complaintdetail)
        if inserted:
            messagebox.showinfo("Success", "Complaint submitted successfully")
            self.load_complaint_history()

    def load_complaint_history(self):
        # Get apartment number from the entry
        apartmentnumber = self.EntryAPID.get()
        # If no apartment number entered, do nothing yet
        if not apartmentnumber:
            return
        # Get tenant ID from the model
        tenantID = self.models.get_tenantID(apartmentnumber)
        if not tenantID:
            return

        # Get complaints from the model
        complaints = self.models.get_recent_complaints(tenantID)

        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert rows
        for complaint in Complaints:
            reason = complaint["reason"]
            timestamp = complaint["timestamp"]
            severity = complaint["severity"]
            status = complaint["status"]
            self.tree.insert("", "end", values=(reason, timestamp, severity, status))

    def create_form(self):
        self.form = ctk.CTkFrame(self, fg_color=BACKGROUND)
        self.form.grid(row=0, column=1, sticky="nsew")
        self.form.grid_columnconfigure(3, weight=1)
        #form start
        title_label = ctk.CTkLabel(self.form, text="Complaints", text_color=TEXT_PRIMARY, font=TITLE_FONT)
        title_label.grid(row = 0, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        # complaint reason
        self.labelcomplaint = ctk.CTkLabel(self.form,font=SUBHEADING_FONT, text_color=TEXT_PRIMARY, text="Complaint Reason:")
        self.labelcomplaint.grid(row = 1, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.Entrycomplaint = ctk.CTkEntry(self.form,width=200, bg_color=SECONDARY, fg_color=SURFACE, placeholder_text="Enter Complaint Reason")
        self.Entrycomplaint.grid(row = 1, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #severity of complaint
        self.labelseverity = ctk.CTkLabel(self.form, font=SUBHEADING_FONT, text_color=TEXT_PRIMARY, text="Severity of Complaint:")
        self.labelseverity.grid(row = 2, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.severity = ctk.CTkOptionMenu(self.form, fg_color=PRIMARY,values=["1", "2", "3", "4", "5"])
        self.severity.grid(row = 2, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #apartment Id entry
        self.labelAPID = ctk.CTkLabel(self.form,font=SUBHEADING_FONT, text_color=TEXT_PRIMARY, text="Apartment Number:") 
        self.labelAPID.grid(row = 3, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.EntryAPID = ctk.CTkEntry(self.form,fg_color=SURFACE,placeholder_text="Enter your Apartment Number")
        self.EntryAPID.grid(row = 3, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.labelComplaintDetails = ctk.CTkLabel(self.form, font=SUBHEADING_FONT, text_color=TEXT_PRIMARY, text="Complaint Details:")
        self.labelComplaintDetails.grid(row = 4, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.EntryComplaintDetails = ctk.CTkTextbox(self.form,width=200, height=100, fg_color=SURFACE)
        self.EntryComplaintDetails.grid(row = 4, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew") 

        button = ctk.CTkButton(self.form,
                               fg_color=PRIMARY,
                               hover_color=PRIMARY_DARK,
                               text="Submit a Complaint",
                               command=self.submit_complaint
                               )
        button.grid(row = 5, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #complaint history
        history_label = ctk.CTkLabel(self.form, font=HEADING_FONT, text_color=TEXT_PRIMARY, text="Complaint History")
        history_label.grid(row = 7, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")

        columns = ("Complaint Number: ", "Report Date", "Severity", "Status")

        self.tree = ttk.Treeview(self.form, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.grid(row = 8, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        self.load_complaint_history()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Complaints Page")
    root.geometry("1000x700")
    complaints_page = ComplaintsPage(root)
    complaints_page.pack(fill="both", expand=True)
    root.mainloop()
    