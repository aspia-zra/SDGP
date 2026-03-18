import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import customtkinter as ctk
from models import theme
from db.db_connect import Database
from gui.page_mdash import DashboardPage
from gui.page_repairs import RepairsPage
from gui.page_complaints import ComplaintsPage


class App:

    def __init__(self, root, db):

        self.root = root
        self.db = db
        self.navbar_mode = "maintenance_dashboard"

        root.app_controller = self
        root.open_maintenance_dashboard = self.show_dashboard
        root.open_repairs_page = self.show_repairs
        root.open_complaints_page = self.show_complaints
        root.open_settings = self.show_settings

        self.show_dashboard()


    def clear(self):

        for w in self.root.winfo_children():
            w.destroy()

    def show_dashboard(self):

        self.clear()
        DashboardPage(self.root, self.db).pack(fill="both", expand=True)

    def show_repairs(self):

        self.clear()
        RepairsPage(self.root, self.db).pack(fill="both", expand=True)

    def show_complaints(self):

        self.clear()
        ComplaintsPage(self.root, self.db).pack(fill="both", expand=True)

    def show_settings(self):

        messagebox.showinfo("Settings", "Settings are not available yet.")

    def logout(self):

        self.root.destroy()


if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = tk.Tk()
    root.title("Maintenance System")
    root.geometry("1000x700")
    root.configure(bg=theme.BACKGROUND)

    db = Database()

    App(root, db)

    root.mainloop()
