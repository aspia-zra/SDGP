# shared file for everyone

from tkinter import *
import matplotlib
import customtkinter as ctk
from . import Admindash, settings
from models.logincode import UserTbl
import theme

class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.SECONDARY)
        self.controller = controller

        self.grid(row=0, column=0, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_navbar()
        
    # these are the different navbars - each function is a navbar we call for each page/dashboard
     
    def admin_nav(self):
        self.navbar = ctk.CTkFrame(self, fg_color="transparent")
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_rowconfigure(7, weight=1)
        self.navbar.grid_columnconfigure(0, weight=1)

        #TITLE
        navtitle_label = ctk.CTkLabel(
            self.navbar, 
            text="Paragon Apartments", 
            fg_color= "transparent",
            text_color=theme.PRIMARY,
            font=(theme.TITLE_FONT, 20))
        navtitle_label.grid(row = 0, column = 0, padx = 20, pady = (20,40), sticky="w")

        btnConfig = { # Styling for buttons here
            "fg_color": theme.PRIMARY,
            "hover_color": theme.PRIMARY_DARK,
            "text_color": theme.SURFACE,
            "height": 40,
            "corner_radius": 8,
            "anchor": "w",
        }

        dashboard = ctk.CTkButton(self.navbar,
            command = self.open_admindash,
            text="Dashboard", **btnConfig)
        dashboard.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        notif = ctk.CTkButton(self.navbar, 
            text="Notifications", **btnConfig)
        notif.grid(row = 2, column = 0, padx = 20, pady = 20, sticky = "ew")

        payments = ctk.CTkButton(self.navbar, 
            text="Payments", **btnConfig)
        payments.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(self.navbar, 
            text="Complaints", **btnConfig)
        complaints.grid(row = 5, column = 0, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(self.navbar, 
            text="Repairs", **btnConfig)
        repairs.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "ew")

        settings = ctk.CTkButton(self.navbar, 
            command = self.open_settings,
            text="Settings", **btnConfig)
        settings.grid(row = 3, column = 0, padx = 20, pady = 20, sticky = "ew")

        logout = ctk.CTkButton(self.navbar, 
            fg_color=theme.PRIMARY, 
            hover_color=theme.DANGER, 
            text="Logout", 
            command = self.logoutbtn)
        logout.grid(row = 8, column = 0, padx = 20, pady = 20, sticky = "s")
    
    def mng_nav(self):
        self.navbar = ctk.CTkFrame(self, fg_color="transparent")
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_rowconfigure(7, weight=1)
        self.navbar.grid_columnconfigure(0, weight=1)

        #TITLE
        navtitle_label = ctk.CTkLabel(
            self.navbar, 
            text="Paragon Apartments", 
            fg_color= "transparent",
            text_color=theme.PRIMARY,
            font=(theme.TITLE_FONT, 20))
        navtitle_label.grid(row = 0, column = 0, padx = 20, pady = (20,40), sticky="w")

        btnConfig = { # Styling for buttons here
            "fg_color": theme.PRIMARY,
            "hover_color": theme.PRIMARY_DARK,
            "text_color": theme.SURFACE,
            "height": 40,
            "corner_radius": 8,
            "anchor": "w",
        }

        dashboard = ctk.CTkButton(self.navbar,
            command = self.open_admindash,
            text="Admin View", **btnConfig)
        dashboard.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        payments = ctk.CTkButton(self.navbar, 
            text="Payments", **btnConfig)
        payments.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(self.navbar, 
            text="Complaints", **btnConfig)
        complaints.grid(row = 5, column = 0, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(self.navbar, 
            text="Repairs", **btnConfig)
        repairs.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "ew")

        reports = ctk.CTkButton(self.navbar, 
            text="Reports", **btnConfig)
        repairs.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "ew")
        
        settings = ctk.CTkButton(self.navbar, 
            command = self.open_settings,
            text="Settings", **btnConfig)
        settings.grid(row = 3, column = 0, padx = 20, pady = 20, sticky = "ew")

        logout = ctk.CTkButton(self.navbar, 
            fg_color=theme.PRIMARY, 
            hover_color=theme.DANGER, 
            text="Logout", 
            command = self.logoutbtn)
        logout.grid(row = 8, column = 0, padx = 20, pady = 20, sticky = "s")    

    
    # these are definitions for the buttons. only these buttons work for now
    
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

