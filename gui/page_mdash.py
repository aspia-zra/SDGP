import customtkinter as ctk
from tkinter import *
from models.repairs import Repair
from gui.mnav import create_navbar


# theme palette
PRIMARY = "#6B4EFF"
PRIMARY_LIGHT = "#9B7EFF"
PRIMARY_DARK = "#4A2FCC"
BACKGROUND = "#F3E8FF"  # light purple background
SURFACE = "#E6DEFF"     # slightly darker light purple cards
TEXT_PRIMARY = "#1A1A2E"
TEXT_SECONDARY = "#4A4A6A"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
INFO = "#3B82F6"

# dashboard style constants (mapped from palette)
BG_COLOR = BACKGROUND
CARD_COLOR = SURFACE
TEXT_COLOR = TEXT_PRIMARY
ACCENT_COLOR = PRIMARY

TITLE_FONT = ("Helvetica", 24, "bold")
HEADING_FONT = ("Helvetica", 18, "bold")
SUBHEADING_FONT = ("Helvetica", 14, "bold")
BODY_FONT = ("Helvetica", 12)
SMALL_FONT = ("Helvetica", 10)

# legacy names used in the code
FONT_TITLE = TITLE_FONT
FONT_HEADER = HEADING_FONT
FONT_LABEL = BODY_FONT
FONT_BTN = SMALL_FONT

def dashboard(parent, db):

    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg=BACKGROUND)

    page = ctk.CTkFrame(parent)
    page.pack(fill="both", expand=True)

    page.grid_rowconfigure(0, weight=1)
    page.grid_columnconfigure(1, weight=1)

    def show_dashboard():
        dashboard(parent, db)

    def show_repairs():
        from gui.page_repairs import RepairsPage

        for w in parent.winfo_children():
            w.destroy()

        RepairsPage(parent, db).pack(fill="both", expand=True)

    def show_complaints():
        from gui.page_complaints import ComplaintsPage

        for w in parent.winfo_children():
            w.destroy()

        ComplaintsPage(parent, db).pack(fill="both", expand=True)

    def show_settings():
        try:
            from . import settings
        except ImportError:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Settings", "Settings are not available yet.")
            return

        for w in parent.winfo_children():
            w.destroy()

        settings.settings(parent)

    create_navbar(page, show_dashboard, show_repairs, show_complaints, show_settings)

    # main content area (same as repairs container)
    container = ctk.CTkFrame(page)
    container.grid(row=0, column=1, sticky="nsew", padx=40, pady=20)

    title = ctk.CTkLabel(
        container,
        text="Maintenance Dashboard",
        font=FONT_TITLE
    )
    title.pack(pady=30)

    dashboardFrame = ctk.CTkFrame(container, fg_color=BG_COLOR)
    dashboardFrame.pack(pady=20)

    dashboardFrame.columnconfigure(0, weight=1)
    dashboardFrame.columnconfigure(1, weight=1)

    # open requests
    openFrame = ctk.CTkFrame(dashboardFrame, fg_color=CARD_COLOR, corner_radius=10)
    openFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    Label(openFrame, text="Open Requests",
          font=FONT_HEADER, bg=CARD_COLOR).grid(row=0, column=0, columnspan=6, pady=10)

    headers = ["Issue", "Apartment", "Date", "Worker", "Priority", ""]
    for i, h in enumerate(headers):
        Label(openFrame, text=h, font=FONT_LABEL,
              bg=CARD_COLOR).grid(row=1, column=i, padx=5, pady=5)

    requests = Repair.get_openrequests(db)

    for idx, r in enumerate(requests):

        row = idx + 2

        Label(openFrame, text=r["id"], bg=CARD_COLOR).grid(row=row, column=0)
        Label(openFrame, text=r["apartment"], bg=CARD_COLOR).grid(row=row, column=1)
        Label(openFrame, text=r["date"], bg=CARD_COLOR).grid(row=row, column=2)
        Label(openFrame, text=r["worker"], bg=CARD_COLOR).grid(row=row, column=3)
        Label(openFrame, text=r["priority"], bg=CARD_COLOR).grid(row=row, column=4)

    # completed jobs
    completedFrame = ctk.CTkFrame(dashboardFrame, fg_color=CARD_COLOR, corner_radius=10)
    completedFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    Label(completedFrame, text="Completed Jobs",
          font=FONT_HEADER, bg=CARD_COLOR).grid(row=0, column=0, columnspan=4, pady=10)

    headers = ["Issue", "Apartment", "Time", "Cost"]
    for i, h in enumerate(headers):
        Label(completedFrame, text=h, font=FONT_LABEL,
              bg=CARD_COLOR).grid(row=1, column=i, padx=5, pady=5)

    jobs = Repair.get_completed_requests(db)

    for idx, j in enumerate(jobs):

        row = idx + 2

        Label(completedFrame, text=j["id"], bg=CARD_COLOR).grid(row=row, column=0)
        Label(completedFrame, text=j["apartment"], bg=CARD_COLOR).grid(row=row, column=1)

        time = j.get("timeTaken", "-")
        cost = j.get("cost", "-")

        Label(completedFrame, text=time, bg=CARD_COLOR).grid(row=row, column=2)
        Label(completedFrame, text=cost, bg=CARD_COLOR).grid(row=row, column=3)
