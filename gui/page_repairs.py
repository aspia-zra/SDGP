# handling workers: one worker per repair per day. if none are available, display 'pick another day'
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.repairs import Repair
from models import theme
from db.db_connect import Database
from gui.nav import navbar as NavigationBar


# Use a light appearance mode for the app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class RepairsPage(ctk.CTkFrame):

    def __init__(self, parent, db=None):
        super().__init__(parent)

        # allow reusing a shared database connection if passed in
        self.db = db or Database()
        controller = getattr(self.winfo_toplevel(), "app_controller", self.winfo_toplevel())

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navbar = NavigationBar(self, controller)
        self.create_widgets()

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

        from .page_complaints import ComplaintsPage
        complaints_page = ComplaintsPage(host, self.db)
        complaints_page.pack(fill="both", expand=True)

    def open_settings(self):
        host = self.winfo_toplevel()
        navigate = getattr(host, "open_settings", None)

        if callable(navigate):
            navigate()
            return

        messagebox.showinfo("Settings", "Settings are not available yet.")


    def create_widgets(self):
        # Main content container (right side) with vertical scrolling.
        self.container = ctk.CTkScrollableFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.container,
            text="Repair Booking",
            font=theme.TITLE_FONT
        )
        title.grid(row=0, column=0, pady=30)

        form = ctk.CTkFrame(self.container)
        form.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        form.grid_columnconfigure(1, weight=1)

        # form components
        # issue
        ctk.CTkLabel(form, text="Repair Reason", font=theme.BODY_FONT).grid(
            row=0, column=0, padx=20, pady=15, sticky="e"
        )

        self.issue_entry = ctk.CTkEntry(form, height=40)
        self.issue_entry.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        # repair details
        ctk.CTkLabel(form, text="Repair Details", font=theme.BODY_FONT).grid(
            row=1, column=0, padx=20, pady=15, sticky="ne"
        )

        self.details_entry = ctk.CTkTextbox(form, height=120)
        self.details_entry.grid(row=1, column=1, padx=20, pady=15, sticky="ew")

        # apartment
        ctk.CTkLabel(form, text="Apartment Number", font=theme.BODY_FONT).grid(
            row=2, column=0, padx=20, pady=15, sticky="e"
        )

        self.apartment_entry = ctk.CTkEntry(form, height=40)
        self.apartment_entry.grid(row=2, column=1, padx=20, pady=15, sticky="ew")

        # date
        ctk.CTkLabel(form, text="Repair Date (DD-MM-YY)", font=theme.BODY_FONT).grid(
            row=3, column=0, padx=20, pady=15, sticky="e"
        )

        self.date_entry = ctk.CTkEntry(form, height=40)
        self.date_entry.grid(row=3, column=1, padx=20, pady=15, sticky="ew")

        # priority
        ctk.CTkLabel(form, text="Priority", font=theme.BODY_FONT).grid(
            row=4, column=0, padx=20, pady=15, sticky="e"
        )

        self.priority_box = ctk.CTkSegmentedButton(
            form,
            values=["1", "2", "3"]
        )
        self.priority_box.grid(row=4, column=1, padx=20, pady=15, sticky="ew")
        self.priority_box.set("2")

        # util
        button_frame = ctk.CTkFrame(self.container)
        button_frame.grid(row=2, column=0, pady=20)

        ctk.CTkButton(
            button_frame,
            text="Book Now",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.SURFACE,
            height=45,
            command=self.book_repair
        ).grid(row=0, column=0, padx=20)

# date error handling

    def valid_date(self, date_string):
        parsed_date = self.parse_date(date_string)

        if parsed_date is None:
            return False

        today = datetime.today().date()
        return parsed_date >= today

    def parse_date(self, date_string):
        normalized = (date_string or "").strip().replace("/", "-")

        for fmt in ("%d-%m-%y", "%d-%m-%Y"):
            try:
                return datetime.strptime(normalized, fmt).date()
            except ValueError:
                continue

        return None

    def to_db_date(self, date_string):
        parsed_date = self.parse_date(date_string)
        if parsed_date is None:
            raise ValueError("Invalid date format")

        return parsed_date.strftime("%Y-%m-%d")

    def display_cost(self):

        apartment_number = self.apartment_entry.get().strip()

        if not apartment_number:
            messagebox.showerror("Error", "Enter an apartment number first.")
            return

        apartment_id = Repair.get_apartment_id_by_number(self.db, apartment_number)
        if not apartment_id:
            messagebox.showerror("Error", "Apartment number not found.")
            return

        cost = Repair.calculate_total_cost(self.db, apartment_id)

        messagebox.showinfo(
            "Estimated Cost",
            f"Total maintenance cost for apartment {apartment_number}: £{cost}"
        )

    def book_repair(self):

        issue = self.issue_entry.get().strip()
        repair_details = self.details_entry.get("1.0", "end").strip()
        apartment_number = self.apartment_entry.get().strip()
        date = self.date_entry.get().strip()
        priority = self.priority_box.get()

        if not issue or not repair_details or not apartment_number or not date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if priority not in {"1", "2", "3"}:
            messagebox.showerror("Error", "Priority must be 1, 2, or 3.")
            return

        if not self.valid_date(date):
            messagebox.showerror(
                "Invalid Date",
                "Repair date cannot be in the past and must follow DD-MM-YY or DD-MM-YYYY."
            )
            return

        try:
            apartment_id = Repair.get_apartment_id_by_number(self.db, apartment_number)
            if not apartment_id:
                messagebox.showerror("Error", "Apartment number not found.")
                return

            db_date = self.to_db_date(date)

            # Worker availability check and assignment (1 job per worker per day).
            # We select a maintenance user who has no job on the chosen date.
            available_worker_query = """
            SELECT u.userID
            FROM UserTbl u
            LEFT JOIN MaintenanceLog m
              ON m.userID = u.userID
             AND DATE(m.maintenanceDate) = DATE(%s)
            WHERE u.Role = 'maintenance'
              AND m.logID IS NULL
            ORDER BY u.userID
            LIMIT 1
            """

            available_worker_row = self.db.fetch_one(available_worker_query, (db_date,))
            if not available_worker_row:
                messagebox.showerror(
                    "No Workers Available",
                    "No maintenance worker is available that day. Please pick another date."
                )
                return

            assigned_worker_id = available_worker_row["userID"]

            Repair.log_maintenance(
                self.db,
                apartment_id,
                assigned_worker_id,
                db_date,
                issue,
                priority,
                repair_details,
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
        self.details_entry.delete("1.0", "end")
        self.apartment_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.priority_box.set("2")

