from tkinter import *
import matplotlib
import customtkinter as ctk

from gui import Admindash, settings
from gui.pages_mngdash import mngdashboard
from models import user_session
# from . import Admindash, settings
# from models.logincode import UserTbl
from . import theme

BG_COLOR = theme.BACKGROUND

class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller, mode="manager"):
        super().__init__(parent, fg_color=theme.SECONDARY)
        self.controller = controller
        self.mode = mode

        self.grid(row=0, column=0, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if self.mode == "admin":
            self.admin_nav()
        else:
            self.mng_nav()
        
        
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

        if user_session.user_type == "manager":
            dashboard_text = "Apartment Management"
            dashboard_command = self.open_mngdash
        else:
            dashboard_text = "Dashboard"
            dashboard_command = self.open_admindash

        dashboard = ctk.CTkButton(self.navbar,
            command = dashboard_command,
            text=dashboard_text, **btnConfig)
        dashboard.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        reports = ctk.CTkButton(self.navbar, 
            text="Reports View", **btnConfig)
        reports.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "ew")

        maintenance = ctk.CTkButton(self.navbar, 
            text="Maintenance View", **btnConfig)
        maintenance.grid(row = 5, column = 0, padx = 20, pady = 20, sticky = "ew")

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

        reports = ctk.CTkButton(self.navbar, 
            text="Reports View", **btnConfig)
        reports.grid(row = 2, column = 0, padx = 20, pady = 20, sticky = "ew")

        maintenance = ctk.CTkButton(self.navbar, 
            text="Maintenance View", **btnConfig)
        maintenance.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "ew")
        
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
    

    def open_mngdash(self): 
        self.controller.clear_page()
        self.controller.current_page = mngdashboard(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_admindash(self): 
        self.controller.clear_page()
        self.controller.current_page = Admindash.admindashboard(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_settings(self):
        self.controller.clear_page()
        self.controller.current_page = settings.settings(self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def logoutbtn(self):
        # UserTbl.logout()
        self.controller.show_login()