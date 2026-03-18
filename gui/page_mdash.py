import customtkinter as ctk
from tkinter import *
from models.repairs import Repair
from models import theme
from gui.nav import navbar as NavigationBar


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, db=None):
        super().__init__(parent)
        self.db = db
        controller = getattr(self.winfo_toplevel(), "app_controller", self.winfo_toplevel())

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        NavigationBar(self, controller)
        self._build()

    def _build(self):
        # main content area
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)

        title = ctk.CTkLabel(
            container,
            text="Maintenance Dashboard",
            font=theme.TITLE_FONT
        )
        title.pack(pady=30)

        dashboardFrame = ctk.CTkFrame(container, fg_color=theme.BACKGROUND)
        dashboardFrame.pack(pady=20)

        dashboardFrame.columnconfigure(0, weight=1)
        dashboardFrame.columnconfigure(1, weight=1)

        # open requests
        openFrame = ctk.CTkFrame(dashboardFrame, fg_color=theme.SURFACE, corner_radius=10)
        openFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        Label(openFrame, text="Open Requests",
              font=theme.HEADING_FONT, bg=theme.SURFACE).grid(row=0, column=0, columnspan=6, pady=10)

        headers = ["Issue", "Apartment", "Date", "Worker", "Priority", ""]
        for i, h in enumerate(headers):
            Label(openFrame, text=h, font=theme.BODY_FONT,
                  bg=theme.SURFACE).grid(row=1, column=i, padx=5, pady=5)

        requests = Repair.get_openrequests(self.db)

        for idx, r in enumerate(requests):
            row = idx + 2
            Label(openFrame, text=r["id"], bg=theme.SURFACE).grid(row=row, column=0)
            Label(openFrame, text=r["apartment"], bg=theme.SURFACE).grid(row=row, column=1)
            Label(openFrame, text=r["date"], bg=theme.SURFACE).grid(row=row, column=2)
            Label(openFrame, text=r["worker"], bg=theme.SURFACE).grid(row=row, column=3)
            Label(openFrame, text=r["priority"], bg=theme.SURFACE).grid(row=row, column=4)

        # completed jobs
        completedFrame = ctk.CTkFrame(dashboardFrame, fg_color=theme.SURFACE, corner_radius=10)
        completedFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        Label(completedFrame, text="Completed Jobs",
              font=theme.HEADING_FONT, bg=theme.SURFACE).grid(row=0, column=0, columnspan=4, pady=10)

        headers = ["Issue", "Apartment", "Time", "Cost"]
        for i, h in enumerate(headers):
            Label(completedFrame, text=h, font=theme.BODY_FONT,
                  bg=theme.SURFACE).grid(row=1, column=i, padx=5, pady=5)

        jobs = Repair.get_completed_requests(self.db)

        for idx, j in enumerate(jobs):
            row = idx + 2
            Label(completedFrame, text=j["id"], bg=theme.SURFACE).grid(row=row, column=0)
            Label(completedFrame, text=j["apartment"], bg=theme.SURFACE).grid(row=row, column=1)

            time = j.get("timeTaken", "-")
            cost = j.get("cost", "-")

            Label(completedFrame, text=time, bg=theme.SURFACE).grid(row=row, column=2)
            Label(completedFrame, text=cost, bg=theme.SURFACE).grid(row=row, column=3)
