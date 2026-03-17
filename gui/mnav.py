# top nav ...
from tkinter import *
import customtkinter as ctk

BG_COLOR = "#f5f3ff"
NAV_COLOR = "#ffffff"
TEXT_COLOR = "#1f1f1f"
ACCENT_COLOR = "#7c3aed"

FONT_BTN = ("Segoe UI", 10, "bold")


def navbar(root, show_dashboard, show_repairs, show_complaints):

    root.configure(bg=BG_COLOR)

    nav = Frame(root, bg=NAV_COLOR, height=60)
    nav.pack(fill="x")

    Button(
        nav,
        text="Dashboard",
        font=FONT_BTN,
        bg=NAV_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        command=show_dashboard
    ).pack(side="left", padx=20, pady=15)

    Button(
        nav,
        text="Repairs",
        font=FONT_BTN,
        bg=NAV_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        command=show_repairs
    ).pack(side="left", padx=20)

    Button(
        nav,
        text="Complaints",
        font=FONT_BTN,
        bg=NAV_COLOR,
        fg=TEXT_COLOR,
        bd=0,
        command=show_complaints
    ).pack(side="left", padx=20)

    content = Frame(root, bg=BG_COLOR)
    content.pack(fill="both", expand=True)

    return content


def create_navbar(parent, show_dashboard, show_repairs, show_complaints, show_settings=None):
    """Create a reusable sidebar navigation bar for the app."""

    navbar = ctk.CTkFrame(parent, width=200)
    navbar.grid(row=0, column=0, sticky="ns")
    navbar.grid_columnconfigure(0, weight=1)

    navtitle_label = ctk.CTkLabel(navbar, text="Paragon Apartments", font=("Arial", 24))
    navtitle_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    dashboard_btn = ctk.CTkButton(navbar, fg_color="#202e75", hover_color="#0f0f30", text="Dashboard", command=show_dashboard)
    dashboard_btn.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

    settings_btn = ctk.CTkButton(
        navbar,
        fg_color="#202e75",
        hover_color="#0f0f30",
        text="Settings",
        command=show_settings if show_settings is not None else (lambda: None)
    )
    settings_btn.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

    complaints = ctk.CTkButton(navbar, fg_color="#202e75", hover_color="#0f0f30", text="Complaints", command=show_complaints)
    complaints.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    repairs = ctk.CTkButton(navbar, fg_color="#202e75", hover_color="#0f0f30", text="Repairs", command=show_repairs)
    repairs.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

    logout = ctk.CTkButton(navbar, fg_color="#202e75", hover_color="#7a070d", text="Logout")
    logout.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

    return navbar
