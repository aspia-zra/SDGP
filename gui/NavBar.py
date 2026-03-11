from tkinter import *
import matplotlib
import customtkinter as ctk
from . import Admindash, settings
from Models.logincode import UserTbl

#Themes- work on font
BG_COLOR = "#f5f3ff"
SIDEBAR_COLOR = "#ede9fe"
CARD_COLOR = "#ffffff"
ACCENT_COLOR = "#7c3aed"
SUB_ACCENT = "#a78bfa"
TEXT_COLOR = "#1f1f1f"
ENTRY_BG = "#f3e8ff"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")

class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.grid(row=0, column=0, sticky="ns")

        self.create_navbar()
        
    def create_navbar(self):
        self.navbar = ctk.CTkFrame(self, width=200)
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_columnconfigure(0, weight=1)

        #nav bar 
        navtitle_label = ctk.CTkLabel(
            self.navbar, 
            text="Paragon Apartments", 
            font=("Arial", 24))
        navtitle_label.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20,)

        dashboard = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#0f0f30",
            command = self.open_admindash,
            text="Dashboard")
        dashboard.grid(row = 1, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        notif = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#0f0f30",
            text="Notifications")
        notif.grid(row = 2, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        settings = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#0f0f30", 
            command = self.open_settings,
            text="Settings")
        settings.grid(row = 3, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        payments = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#0f0f30", 
            text="Payments")
        payments.grid(row = 4, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#0f0f30", 
            text="Complaints")
        complaints.grid(row = 5, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#0f0f30", 
            text="Repairs")
        repairs.grid(row = 6, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")

        logout = ctk.CTkButton(
            self.navbar, 
            fg_color="#202e75", 
            hover_color="#7a070d", 
            text="Logout", 
            command = self.logoutbtn)
        logout.grid(row = 8, column = 0, columnspan = 1, padx = 20, pady = 20, sticky = "ew")
    
    def open_admindash(self):
        self.controller.clear_page()
        self.controller.current_page = Admindash.admindashboard(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_settings(self):
        self.controller.clear_page()
        self.controller.current_page = settings.settings(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def logoutbtn(self):
        UserTbl.logout()
        self.controller.show_login()