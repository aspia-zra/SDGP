import customtkinter as ctk
from tkinter import messagebox, simpledialog
from models.repairs import Repair
from db.dbconnect import *
from gui.theme import *
import gui.navbar as nav


class RepairsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # navbar
        self.grid_columnconfigure(1, weight=0)  # actions
        self.grid_columnconfigure(2, weight=1)  # main content

        self.nav = nav.navbar(self, controller)
        self.nav.grid(row=0, column=0, sticky="ns")

        self.create_widgets()

    def create_widgets(self):
        sidebar = ctk.CTkFrame(
            self,
            width=240,
            fg_color=SURFACE,
            corner_radius=0
        )
        sidebar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=0)
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="Maintenance",
            font=HEADING_FONT,
            text_color=PRIMARY
        ).grid(row=0, column=0, padx=20, pady=(25, 20), sticky="w")

        buttons = [
            ("Book Maintenance", self.book_maintenance),
            ("Record Resolution", self.record_resolution),
            ("Check Worker Availability", self.check_availability),
            ("Check Worker Role", self.check_role),
            ("Calculate Total Cost", self.calculate_total_cost),
            ("Generate Maintenance Report", self.generate_report),
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=42,
                corner_radius=10,
                font=BODY_FONT,
                fg_color=PRIMARY,
                hover_color=PRIMARY_DARK,
                text_color="white"
            ).grid(row=i, column=0, padx=20, pady=8, sticky="ew")

        sidebar.grid_columnconfigure(0, weight=1)

        self.main_area = ctk.CTkFrame(self, fg_color=BACKGROUND)
        self.main_area.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.main_area,
            text="Maintenance Management",
            text_color=PRIMARY,
            font=TITLE_FONT
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        form_card = ctk.CTkFrame(
            self.main_area,
            fg_color=SURFACE,
            corner_radius=12,
            width=700,
            height=320
        )
        form_card.grid(row=1, column=0, sticky="n", padx=10, pady=10)
        form_card.grid_propagate(False)

        form_card.grid_columnconfigure(0, weight=0)
        form_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            form_card,
            text="Maintenance Details",
            font=HEADING_FONT,
            text_color=PRIMARY
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        labels = ["Apartment ID", "Worker ID", "Maintenance Date (YYYY-MM-DD)"]
        self.entries = {}

        for i, label in enumerate(labels, start=1):
            ctk.CTkLabel(
                form_card,
                text=label,
                font=BODY_FONT,
                text_color=TEXT_PRIMARY
            ).grid(row=i, column=0, sticky="w", padx=20, pady=12)

            entry = ctk.CTkEntry(
                form_card,
                height=40,
                font=BODY_FONT,
                fg_color="white",
                text_color="black",
                border_width=1
            )
            entry.grid(row=i, column=1, sticky="ew", padx=20, pady=12)
            self.entries[label] = entry

        ctk.CTkButton(
            form_card,
            text="Book Maintenance",
            command=self.book_maintenance,
            height=42,
            width=180,
            corner_radius=10,
            font=BODY_FONT,
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            text_color="white"
        ).grid(row=4, column=0, columnspan=2, pady=(20, 20))

    def book_maintenance(self):
        apt = self.entries["Apartment ID"].get().strip()
        worker = self.entries["Worker ID"].get().strip()
        date = self.entries["Maintenance Date (YYYY-MM-DD)"].get().strip()

        if not apt or not worker or not date:
            messagebox.showerror("Error", "Complete all fields.")
            return

        try:
            Repair.log_maintenance(self.db, apt, worker, date)
            messagebox.showinfo("Success", "Maintenance booked!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def record_resolution(self):
        try:
            log_id = simpledialog.askinteger("Log ID", "Enter Log ID:")
            time_taken = simpledialog.askfloat("Time Taken", "Hours spent:")
            cost = simpledialog.askfloat("Cost", "Repair cost:")
            notes = simpledialog.askstring("Notes", "Any notes?")

            if log_id is None or time_taken is None or cost is None:
                return

            Repair.record_resolution(self.db, log_id, time_taken, cost, notes)
            messagebox.showinfo("Success", "Resolution logged!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_availability(self):
        worker = self.entries["Worker ID"].get().strip()
        date = self.entries["Maintenance Date (YYYY-MM-DD)"].get().strip()

        if not worker or not date:
            messagebox.showerror("Error", "Enter Worker ID and Maintenance Date.")
            return

        try:
            available = Repair.check_availability(self.db, worker, date)
            messagebox.showinfo(
                "Worker Availability",
                f"{worker} is {'Available' if available else 'Not available'} on {date}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_role(self):
        worker = self.entries["Worker ID"].get().strip()
        if not worker:
            messagebox.showerror("Error", "Enter Worker ID first.")
            return

        try:
            valid = Repair.check_role(self.db, worker)
            messagebox.showinfo(
                "Worker Role Check",
                f"{worker}: {'Correct role' if valid else 'Incorrect role'}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_total_cost(self):
        apt = self.entries["Apartment ID"].get().strip()
        if not apt:
            messagebox.showerror("Error", "Enter Apartment ID.")
            return

        try:
            total = Repair.calculate_total_cost(self.db, apt)
            messagebox.showinfo("Total Cost", f"Total maintenance cost for {apt}: {total}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_report(self):
        apt = self.entries["Apartment ID"].get().strip()
        if not apt:
            messagebox.showerror("Error", "Enter Apartment ID.")
            return

        try:
            logs = Repair.generate_report(self.db)

            report_text = ""
            for log in logs:
                report_text += (
                    f"LogID: {log['logID']}, "
                    f"AptID: {log['apartmentID']}, "
                    f"WorkerID: {log['userID']}, "
                    f"Date: {log['maintenanceDate']}, "
                    f"Cost: {log['Cost']}, "
                    f"Notes: {log['Notes']}\n"
                )

            report_window = ctk.CTkToplevel(self)
            report_window.title("Maintenance Report")
            report_window.geometry("900x500")

            textbox = ctk.CTkTextbox(
                report_window,
                font=BODY_FONT,
                text_color="black",
                fg_color="white"
            )
            textbox.pack(fill="both", expand=True, padx=20, pady=20)
            textbox.insert("1.0", report_text)

        except Exception as e:
            messagebox.showerror("Error", str(e))
