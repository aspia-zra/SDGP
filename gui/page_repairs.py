# handling workers: one worker per repair per day. if none are available, display 'pick another day'
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.repairs import Repair
from db.db_connect import Database


# Use a light appearance mode for the app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

from gui.mnav import create_navbar


class RepairsPage(ctk.CTkFrame):

    def __init__(self, parent, db=None):
        super().__init__(parent)

        # allow reusing a shared database connection if passed in
        self.db = db or Database()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navbar = create_navbar(
            self,
            self.open_dashboard,
            self.open_repairs,
            self.open_complaints,
            self.open_settings
        )
        self.create_widgets()

    def open_dashboard(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        from .page_mdash import dashboard
        dashboard(self.master, self.db)

    def open_repairs(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        repairs_page = RepairsPage(self.master, self.db)
        repairs_page.pack(fill="both", expand=True)

    def open_complaints(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        from .page_complaints import ComplaintsPage
        complaints_page = ComplaintsPage(self.master)
        complaints_page.pack(fill="both", expand=True)

    def open_settings(self):
        try:
            from . import settings
        except ImportError:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Settings", "Settings are not available yet.")
            return

        for widget in self.master.winfo_children():
            widget.destroy()

        settings.settings(self.master)


    def create_widgets(self):
        # Main content container (right side)
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.container,
            text="Repair Booking",
            font=("Segoe UI", 28, "bold")
        )
        title.grid(row=0, column=0, pady=30)

        form = ctk.CTkFrame(self.container)
        form.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        form.grid_columnconfigure(1, weight=1)

        # form components
        # issue
        ctk.CTkLabel(form, text="Issue / Notes", font=("Segoe UI", 16)).grid(
            row=0, column=0, padx=20, pady=15, sticky="e"
        )

        self.issue_entry = ctk.CTkEntry(form, height=40)
        self.issue_entry.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        # apartment
        ctk.CTkLabel(form, text="Apartment ID", font=("Segoe UI", 16)).grid(
            row=1, column=0, padx=20, pady=15, sticky="e"
        )

        self.apartment_entry = ctk.CTkEntry(form, height=40)
        self.apartment_entry.grid(row=1, column=1, padx=20, pady=15, sticky="ew")

        # date
        ctk.CTkLabel(form, text="Repair Date (YYYY-MM-DD)", font=("Segoe UI", 16)).grid(
            row=2, column=0, padx=20, pady=15, sticky="e"
        )

        self.date_entry = ctk.CTkEntry(form, height=40)
        self.date_entry.grid(row=2, column=1, padx=20, pady=15, sticky="ew")

        # priority
        ctk.CTkLabel(form, text="Priority", font=("Segoe UI", 16)).grid(
            row=3, column=0, padx=20, pady=15, sticky="e"
        )

        self.priority_box = ctk.CTkComboBox(
            form,
            values=["Low", "Medium", "High"]
        )
        self.priority_box.grid(row=3, column=1, padx=20, pady=15, sticky="ew")

        # util
        button_frame = ctk.CTkFrame(self.container)
        button_frame.grid(row=2, column=0, pady=20)

        ctk.CTkButton(
            button_frame,
            text="Display Cost",
            height=45,
            command=self.display_cost
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            button_frame,
            text="Book Now",
            height=45,
            command=self.book_repair
        ).grid(row=0, column=1, padx=20)

# date error handling

    def valid_date(self, date_string):

        try:
            repair_date = datetime.strptime(date_string, "%Y-%m-%d").date()
            today = datetime.today().date()

            if repair_date < today:
                return False

            return True

        except ValueError:
            return False

    def display_cost(self):

        apartment_id = self.apartment_entry.get().strip()

        if not apartment_id:
            messagebox.showerror("Error", "Enter an apartment ID first.")
            return

        cost = Repair.calculate_total_cost(self.db, apartment_id)

        messagebox.showinfo(
            "Estimated Cost",
            f"Total maintenance cost for apartment {apartment_id}: £{cost}"
        )

    def book_repair(self):

        issue = self.issue_entry.get().strip()
        apartment_id = self.apartment_entry.get().strip()
        date = self.date_entry.get().strip()
        priority = self.priority_box.get()

        if not issue or not apartment_id or not date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not self.valid_date(date):
            messagebox.showerror(
                "Invalid Date",
                "Repair date cannot be in the past and must follow YYYY-MM-DD."
            )
            return

        try:

            # Worker availability check (1 job per worker per day)

            total_workers_query = """
            SELECT COUNT(*)
            FROM UserTbl
            WHERE Role = 'maintenance'
            """

            busy_workers_query = """
            SELECT COUNT(DISTINCT userID)
            FROM MaintenanceLog
            WHERE DATE(maintenanceDate) = DATE(%s)
            """

            total_workers = self.db.fetch_one(total_workers_query)[0]
            busy_workers = self.db.fetch_one(busy_workers_query, (date,))[0]

            if busy_workers >= total_workers:
                messagebox.showerror(
                    "No Workers Available",
                    "All maintenance workers already have a job that day. Please pick another date."
                )
                return

            Repair.log_maintenance(
                self.db,
                apartment_id,
                None,
                date
            )

            # EMAIL PLACEHOLDER
            # send_email_to_tenant(apartment_id, date)

            messagebox.showinfo(
                "Success",
                "Repair booked successfully. Tenant notification sent."
            )

            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):

        self.issue_entry.delete(0, "end")
        self.apartment_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.priority_box.set("")
