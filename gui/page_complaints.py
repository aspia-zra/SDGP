import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db.db_connect import Database
from models.complaints import Complaints
from models import theme
from gui.nav import navbar as NavigationBar

class ComplaintsPage(ctk.CTkFrame):
    def __init__(self, parent, db=None):
        super().__init__(parent)

        self.models = Complaints()
        self.db = db or Database()
        controller = getattr(self.winfo_toplevel(), "app_controller", self.winfo_toplevel())

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navbar = NavigationBar(self, controller)
        self.create_form()

    def open_maintenance_dashboard(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_maintenance_dashboard", None)

        if callable(navigate):
            navigate()
            return

        for widget in host.winfo_children():
            widget.destroy()

        from .page_mdash import dashboard
        dashboard(host, self.db)

    def open_repairs(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_repairs_page", None)

        if callable(navigate):
            navigate()
            return

        for widget in host.winfo_children():
            widget.destroy()

        from .page_repairs import RepairsPage
        repairs_page = RepairsPage(host, self.db)
        repairs_page.pack(fill="both", expand=True)

    def open_complaints(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_complaints_page", None)

        if callable(navigate):
            navigate()
            return

        for widget in host.winfo_children():
            widget.destroy()

        complaints_page = ComplaintsPage(host, self.db)
        complaints_page.pack(fill="both", expand=True)

    def open_settings(self):
        try:
            from . import settings
        except ImportError:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Settings", "Settings are not available yet.")
            return

        host = self.winfo_toplevel()

        for widget in host.winfo_children():
            widget.destroy()

        settings.settings(host)

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
        for complaint in complaints:
            reason = complaint["reason"]
            timestamp = complaint["timestamp"]
            severity = complaint["severity"]
            status = complaint["status"]
            self.tree.insert("", "end", values=(reason, timestamp, severity, status))

    
    def create_form(self):
        self.form = ctk.CTkFrame(self)
        self.form.grid(row=0, column=1, sticky="nsew")
        self.form.grid_columnconfigure(3, weight=1)
        #form start
        title_label = ctk.CTkLabel(self.form, text="Complaints", font=theme.HEADING_FONT)
        title_label.grid(row = 0, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        # complaint reason
        self.labelcomplaint = ctk.CTkLabel(self.form, text="Complaint Reason:")
        self.labelcomplaint.grid(row = 1, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.Entrycomplaint = ctk.CTkEntry(self.form,width=200  , placeholder_text="Enter Complaint Reason")
        self.Entrycomplaint.grid(row = 1, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #severity of complaint
        self.labelseverity = ctk.CTkLabel(self.form, text="Severity of Complaint:")
        self.labelseverity.grid(row = 2, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.severity = ctk.CTkOptionMenu(self.form, values=["1", "2", "3", "4", "5"])
        self.severity.grid(row = 2, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #apartment Id entry
        self.labelAPID = ctk.CTkLabel(self.form, text="Apartment Number:") 
        self.labelAPID.grid(row = 3, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.EntryAPID = ctk.CTkEntry(self.form, placeholder_text="Enter your Apartment Number")
        self.EntryAPID.grid(row = 3, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.labelComplaintDetails = ctk.CTkLabel(self.form, text="Complaint Details:")
        self.labelComplaintDetails.grid(row = 4, column = 2, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        self.EntryComplaintDetails = ctk.CTkTextbox(self.form, width=200, height=100, fg_color=theme.SURFACE, text_color=theme.TEXT_PRIMARY)
        self.EntryComplaintDetails.grid(row = 4, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew") 

        button = ctk.CTkButton(self.form,
                       fg_color=theme.PRIMARY,
                       hover_color=theme.PRIMARY_DARK,
                       text_color=theme.SURFACE,
                       text="Submit a Complaint",
                       command=self.submit_complaint
                       )
        button.grid(row = 5, column = 3, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        #complaint history
        history_label = ctk.CTkLabel(self.form, text="Complaint History", font=theme.HEADING_FONT)
        history_label.grid(row = 7, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")

        columns = ("Complaint Number: ", "Report Date", "Severity", "Status")

        self.tree = ttk.Treeview(self.form, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.grid(row = 8, column = 2, columnspan = 2, padx = 20, pady = 20, sticky = "nsew")
        self.load_complaint_history()
