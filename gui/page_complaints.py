import customtkinter as ctk
import tkinter.messagebox as messagebox
from db.db_connect import Database
from models.complaints import Complaints
from . import theme
from gui.nav import navbar as NavigationBar

class ComplaintsPage(ctk.CTkFrame):
    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=theme.BACKGROUND)

        self.db = db or Database()
        self.models = Complaints(self.db)
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
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_settings", None)

        if callable(navigate):
            navigate()
            return

        messagebox.showinfo("Settings", "Settings are not available yet.")

    def submit_complaint(self):
        reason = self.Entrycomplaint.get()
        severity = self.severity.get()
        apartmentnumber = self.EntryAPID.get()
        complaintdetail = self.EntryComplaintDetails.get("1.0", "end")

        if severity not in {"1", "2", "3"}:
            messagebox.showerror("Error", "Severity must be 1, 2, or 3.")
            return
        
        inserted = self.models.add_complaint(reason, severity, apartmentnumber, complaintdetail)
        if inserted:
            messagebox.showinfo("Success", "Complaint submitted successfully")
        else:
            messagebox.showerror("Error", "Could not submit complaint. Check apartment number and active lease.")

    
    def create_form(self):
        self.form = ctk.CTkFrame(self, fg_color=theme.BACKGROUND)
        self.form.grid(row=0, column=1, sticky="nsew")
        self.form.grid_columnconfigure(3, weight=1)

        content_card = ctk.CTkFrame(self.form, fg_color=theme.SURFACE, corner_radius=12)
        content_card.grid(row=0, column=2, columnspan=2, padx=40, pady=30, sticky="nsew")
        content_card.grid_columnconfigure(1, weight=1)

        #form start
        title_label = ctk.CTkLabel(content_card, text="Complaints", font=theme.TITLE_FONT, text_color=theme.PRIMARY)
        title_label.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = (20, 30), sticky = "nsew")
        # complaint reason
        self.labelcomplaint = ctk.CTkLabel(content_card, text="Complaint Reason:", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY)
        self.labelcomplaint.grid(row = 1, column = 0, columnspan = 1, padx = 20, pady = 12, sticky = "ew")

        self.Entrycomplaint = ctk.CTkEntry(
            content_card,
            width=260,
            placeholder_text="Enter Complaint Reason",
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            placeholder_text_color=theme.TEXT_SECONDARY,
            border_color=theme.SECONDARY,
        )
        self.Entrycomplaint.grid(row = 1, column = 1, columnspan = 1, padx = 20, pady = 12, sticky = "ew")

        #severity of complaint
        self.labelseverity = ctk.CTkLabel(content_card, text="Severity of Complaint:", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY)
        self.labelseverity.grid(row = 2, column = 0, columnspan = 1, padx = 20, pady = 12, sticky = "ew")

        self.severity = ctk.CTkSegmentedButton(
            content_card,
            values=["1", "2", "3"],
            selected_color=theme.PRIMARY,
            selected_hover_color=theme.PRIMARY_DARK,
            unselected_color=theme.BACKGROUND,
            unselected_hover_color=theme.SECONDARY,
            text_color=theme.TEXT_PRIMARY,
        )
        self.severity.grid(row = 2, column = 1, columnspan = 1, padx = 20, pady = 12, sticky = "ew")
        self.severity.set("2")

        #apartment Id entry
        self.labelAPID = ctk.CTkLabel(content_card, text="Apartment Number:", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY) 
        self.labelAPID.grid(row = 3, column = 0, columnspan = 1, padx = 20, pady = 12, sticky = "ew")

        self.EntryAPID = ctk.CTkEntry(
            content_card,
            placeholder_text="Enter your Apartment Number",
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            placeholder_text_color=theme.TEXT_SECONDARY,
            border_color=theme.SECONDARY,
        )
        self.EntryAPID.grid(row = 3, column = 1, columnspan = 1, padx = 20, pady = 12, sticky = "ew")

        self.labelComplaintDetails = ctk.CTkLabel(content_card, text="Complaint Details:", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY)
        self.labelComplaintDetails.grid(row = 4, column = 0, columnspan = 1, padx = 20, pady = 12, sticky = "ew")

        self.EntryComplaintDetails = ctk.CTkTextbox(
            content_card,
            width=260,
            height=120,
            fg_color=theme.BACKGROUND,
            text_color=theme.TEXT_PRIMARY,
            border_color=theme.SECONDARY,
            border_width=1,
        )
        self.EntryComplaintDetails.grid(row = 4, column = 1, columnspan = 1, padx = 20, pady = 12, sticky = "ew") 

        button = ctk.CTkButton(content_card,
                       fg_color=theme.PRIMARY,
                       hover_color=theme.PRIMARY_DARK,
                       text_color=theme.SURFACE,
                       font=theme.BODY_FONT,
                       text="Submit a Complaint",
                       command=self.submit_complaint
                       )
        button.grid(row = 5, column = 1, columnspan = 1, padx = 20, pady = (20, 24), sticky = "ew")
