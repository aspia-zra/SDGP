import customtkinter as ctk
from tkinter import messagebox
from models.repairs import Repair
from models import theme
from db.db_connect import Database
from gui.nav import navbar as NavigationBar


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        # Keep behavior consistent with other maintenance pages: create a
        # connection when the caller does not inject one.
        self.db = db or Database()
        controller = getattr(self.winfo_toplevel(), "app_controller", self.winfo_toplevel())
        self._ensure_scaling_safe_root()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        NavigationBar(self, controller)
        self.main_container = None
        self._build()

    def _ensure_scaling_safe_root(self):
        root = self.winfo_toplevel()

        if not hasattr(root, "block_update_dimensions_event"):
            root.block_update_dimensions_event = lambda: None

        if not hasattr(root, "unblock_update_dimensions_event"):
            root.unblock_update_dimensions_event = lambda: None

    def _table_header_label(self, parent, text, row, column, anchor="center"):
        ctk.CTkLabel(parent, text=text, font=theme.BODY_FONT, anchor=anchor).grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="ew",
        )

    def _table_value_label(self, parent, text, row, column, wraplength=0, anchor="center"):
        ctk.CTkLabel(parent, text=text, wraplength=wraplength, justify="center", anchor=anchor).grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="ew",
        )

    def _configure_table_columns(self, frame, column_specs):
        for col, (_, width, _) in enumerate(column_specs):
            frame.grid_columnconfigure(col, minsize=width, weight=0)

    def _build(self):
        if self.main_container is not None:
            self.main_container.destroy()

        self.main_container = ctk.CTkFrame(self, fg_color=theme.BACKGROUND)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.main_container,
            text="Maintenance Dashboard",
            font=theme.TITLE_FONT,
        ).grid(row=0, column=0, pady=(20, 20))

        dashboard_frame = ctk.CTkFrame(self.main_container, fg_color=theme.BACKGROUND)
        dashboard_frame.grid(row=1, column=0, sticky="nsew")
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.rowconfigure(0, weight=1)
        dashboard_frame.rowconfigure(1, weight=1)

        open_frame = ctk.CTkFrame(dashboard_frame, fg_color=theme.SURFACE, corner_radius=10)
        open_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        open_frame.grid_columnconfigure(0, weight=1)
        open_frame.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(open_frame, text="Open Requests", font=theme.HEADING_FONT).grid(row=0, column=0, pady=(12, 8))

        open_header_frame = ctk.CTkFrame(open_frame, fg_color=theme.SURFACE)
        open_header_frame.grid(row=1, column=0, sticky="ew", padx=10)
        open_columns = [
            ("Type", 90, "center"),
            ("Apartment", 100, "center"),
            ("Issue", 260, "center"),
            ("Date", 100, "center"),
            ("Worker", 90, "center"),
            ("Priority", 90, "center"),
            ("", 100, "center"),
            ("", 110, "center"),
        ]
        self._configure_table_columns(open_header_frame, open_columns)
        for i, (header, _, anchor) in enumerate(open_columns):
            self._table_header_label(open_header_frame, header, 0, i, anchor=anchor)

        open_scroll = ctk.CTkScrollableFrame(open_frame, fg_color=theme.SURFACE, height=240)
        open_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=(4, 10))
        self._configure_table_columns(open_scroll, open_columns)

        requests = Repair.get_openrequests(self.db)
        for idx, req in enumerate(requests):
            self._table_value_label(open_scroll, req["type"], idx, 0)
            self._table_value_label(open_scroll, req["apartment"], idx, 1)
            self._table_value_label(open_scroll, req.get("issue") or "-", idx, 2, wraplength=320)
            self._table_value_label(open_scroll, req["date"], idx, 3)
            self._table_value_label(open_scroll, req.get("worker") or "-", idx, 4)
            self._table_value_label(open_scroll, req.get("priority") or "-", idx, 5)

            if req.get("type") == "complaint":
                ctk.CTkButton(
                    open_scroll,
                    text="Details",
                    width=90,
                    fg_color=theme.INFO,
                    hover_color=theme.PRIMARY_DARK,
                    text_color=theme.SURFACE,
                    command=lambda selected=req: self._open_open_request_details(selected),
                ).grid(row=idx, column=6, padx=5, pady=5, sticky="e")
            else:
                self._table_value_label(open_scroll, "-", idx, 6)

            ctk.CTkButton(
                open_scroll,
                text="Complete",
                width=90,
                fg_color=theme.PRIMARY,
                hover_color=theme.PRIMARY_DARK,
                text_color=theme.SURFACE,
                command=lambda selected=req: self._open_complete_dialog(selected),
            ).grid(row=idx, column=7, padx=5, pady=5, sticky="e")

        completed_frame = ctk.CTkFrame(dashboard_frame, fg_color=theme.SURFACE, corner_radius=10)
        completed_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        completed_frame.grid_columnconfigure(0, weight=1)
        completed_frame.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(completed_frame, text="Recently Completed", font=theme.HEADING_FONT).grid(row=0, column=0, pady=(12, 8))

        completed_header_frame = ctk.CTkFrame(completed_frame, fg_color=theme.SURFACE)
        completed_header_frame.grid(row=1, column=0, sticky="ew", padx=10)
        completed_columns = [
            ("Type", 90, "center"),
            ("Apartment", 100, "center"),
            ("Issue", 260, "center"),
            ("Date", 100, "center"),
            ("", 130, "center"),
        ]
        self._configure_table_columns(completed_header_frame, completed_columns)
        for i, (header, _, anchor) in enumerate(completed_columns):
            self._table_header_label(completed_header_frame, header, 0, i, anchor=anchor)

        completed_scroll = ctk.CTkScrollableFrame(completed_frame, fg_color=theme.SURFACE, height=240)
        completed_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=(4, 10))
        self._configure_table_columns(completed_scroll, completed_columns)

        jobs = Repair.get_completed_requests(self.db)
        for idx, job in enumerate(jobs):
            self._table_value_label(completed_scroll, job["type"], idx, 0)
            self._table_value_label(completed_scroll, job["apartment"], idx, 1)
            self._table_value_label(completed_scroll, job.get("issue") or "-", idx, 2, wraplength=320)
            self._table_value_label(completed_scroll, job.get("date") or "-", idx, 3)

            ctk.CTkButton(
                completed_scroll,
                text="View Details",
                width=110,
                fg_color=theme.INFO,
                hover_color=theme.PRIMARY_DARK,
                text_color=theme.SURFACE,
                command=lambda selected=job: self._open_details_dialog(selected),
            ).grid(row=idx, column=4, padx=5, pady=5, sticky="e")

    def _open_details_dialog(self, job):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{job['type'].title()} Details")
        dialog.geometry("460x360")
        dialog.configure(fg_color=theme.SURFACE)
        dialog.grab_set()

        details = [
            ("Type", job.get("type", "-")),
            ("Apartment", job.get("apartment", "-")),
            ("Date", job.get("date", "-")),
            ("Issue", job.get("issue", "-")),
            ("Resolution", job.get("resolution", "-")),
        ]

        if job.get("type") == "repair":
            time_taken = job.get("timeTaken")
            cost = job.get("cost")

            if time_taken not in (None, "", "-"):
                details.append(("Time Taken", time_taken))

            if cost not in (None, "", "-"):
                details.append(("Cost", cost))

        body = ctk.CTkTextbox(dialog, width=400, height=260)
        body.pack(padx=20, pady=(20, 10))

        for key, value in details:
            body.insert("end", f"{key}: {value}\n")

        body.configure(state="disabled")

        ctk.CTkButton(
            dialog,
            text="Close",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.SURFACE,
            command=dialog.destroy,
        ).pack(pady=(0, 15))

    def _open_open_request_details(self, request):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Complaint Details")
        dialog.geometry("460x320")
        dialog.configure(fg_color=theme.SURFACE)
        dialog.grab_set()

        details = [
            ("Type", request.get("type", "-")),
            ("Apartment", request.get("apartment", "-")),
            ("Date", request.get("date", "-")),
            ("Issue", request.get("issue", "-")),
            ("Details", request.get("complaintDetails", "-")),
        ]

        body = ctk.CTkTextbox(dialog, width=400, height=220)
        body.pack(padx=20, pady=(20, 10))

        for key, value in details:
            body.insert("end", f"{key}: {value}\n")

        body.configure(state="disabled")

        ctk.CTkButton(
            dialog,
            text="Close",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.SURFACE,
            command=dialog.destroy,
        ).pack(pady=(0, 15))

    def _open_complete_dialog(self, request):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Complete {request['type']} #{request['id']}")
        dialog.geometry("420x340")
        dialog.configure(fg_color=theme.SURFACE)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Time Taken").pack(pady=(20, 5))
        time_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="e.g. 2 hours")
        time_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Cost").pack(pady=(10, 5))
        cost_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="e.g. 120.00")
        cost_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Resolution").pack(pady=(10, 5))
        resolution_entry = ctk.CTkTextbox(dialog, width=300, height=100)
        resolution_entry.pack(pady=5)

        def submit_completion():
            time_text = time_entry.get().strip()
            cost_text = cost_entry.get().strip()
            resolution = resolution_entry.get("1.0", "end").strip()

            if not resolution:
                messagebox.showerror("Validation", "Please enter a resolution.")
                return

            cost = None
            if cost_text:
                try:
                    cost = float(cost_text)
                except ValueError:
                    messagebox.showerror("Validation", "Cost must be a number.")
                    return

            time_taken = None
            if request["type"] == "repair":
                if not time_text:
                    time_taken = 0
                else:
                    try:
                        time_taken = int(time_text)
                    except ValueError:
                        messagebox.showerror("Validation", "Time taken must be a whole number.")
                        return

            Repair.complete_request(
                self.db,
                request["id"],
                request["type"],
                time_taken,
                resolution,
                cost,
            )

            sent, email_message = Repair.send_maintenance_notification(
                self.db,
                request["apartment"],
                request["date"],
            )

            if dialog.winfo_exists():
                dialog.grab_release()
                dialog.withdraw()
                dialog.destroy()

            def finalize_submit():
                self._build()
                if sent:
                    messagebox.showinfo("Notification Sent", email_message, parent=self.winfo_toplevel())
                else:
                    messagebox.showwarning("Notification Not Sent", email_message, parent=self.winfo_toplevel())

            self.after(60, finalize_submit)

        ctk.CTkButton(
            dialog,
            text="Submit",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.SURFACE,
            command=submit_completion,
        ).pack(pady=15)
