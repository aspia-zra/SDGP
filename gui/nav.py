# updated navbar code

# shared file for everyone

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from models import theme

class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.SECONDARY)
        self.controller = controller

        self.grid(row=0, column=0, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_navbar()
        
    def create_navbar(self):
        mode = getattr(self.controller, "navbar_mode", "maintenance_dashboard")

        if mode == "admin":
            self.admin_nav()
            return

        if mode == "management":
            self.mng_nav()
            return

        self.maintenance_dashboard_nav()

    def _reset_navbar(self):
        if hasattr(self, "navbar") and self.navbar.winfo_exists():
            self.navbar.destroy()

        self.navbar = ctk.CTkFrame(self, fg_color="transparent")
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_rowconfigure(7, weight=1)
        self.navbar.grid_columnconfigure(0, weight=1)

        navtitle_label = ctk.CTkLabel(
            self.navbar,
            text="Paragon Apartments",
            fg_color="transparent",
            text_color=theme.PRIMARY,
            font=theme.HEADING_FONT
        )
        navtitle_label.grid(row=0, column=0, padx=20, pady=(20, 40), sticky="w")

    def _nav_button_config(self):
        return {
            "fg_color": theme.PRIMARY,
            "hover_color": theme.PRIMARY_DARK,
            "text_color": theme.SURFACE,
            "height": 40,
            "corner_radius": 8,
            "anchor": "w",
        }

    def _invoke_controller(self, *method_names):
        for method_name in method_names:
            method = getattr(self.controller, method_name, None)
            if callable(method):
                host = getattr(self.controller, "root", None)
                if host is not None and hasattr(host, "after_idle"):
                    host.after_idle(method)
                else:
                    self.after_idle(method)
                return True

        return False
        
    # these are the different navbars - each function is a navbar we call for each page/dashboard
     
    def admin_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        dashboard = ctk.CTkButton(self.navbar,
            command = self.open_admindash,
            text="Dashboard", **btnConfig)
        dashboard.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        notif = ctk.CTkButton(self.navbar, 
            command=lambda: None,
            text="Notifications", **btnConfig)
        notif.grid(row = 2, column = 0, padx = 20, pady = 20, sticky = "ew")

        payments = ctk.CTkButton(self.navbar, 
            command=lambda: None,
            text="Payments", **btnConfig)
        payments.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(self.navbar, 
            command=self.open_complaints,
            text="Complaints", **btnConfig)
        complaints.grid(row = 5, column = 0, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(self.navbar, 
            command=self.open_repairs,
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

    def maintenance_dashboard_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        maintenance_dashboard = ctk.CTkButton(
            self.navbar,
            command=self.open_maintenance_dashboard,
            text="Maintenance Dashboard",
            **btnConfig,
        )
        maintenance_dashboard.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        settings_button = ctk.CTkButton(
            self.navbar,
            command=self.open_settings,
            text="Settings",
            **btnConfig,
        )
        settings_button.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        complaints_button = ctk.CTkButton(
            self.navbar,
            command=self.open_complaints,
            text="Complaints",
            **btnConfig,
        )
        complaints_button.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        repairs_button = ctk.CTkButton(
            self.navbar,
            command=self.open_repairs,
            text="Repairs",
            **btnConfig,
        )
        repairs_button.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        logout = ctk.CTkButton(
            self.navbar,
            fg_color=theme.PRIMARY,
            hover_color=theme.DANGER,
            text="Logout",
            command=self.logoutbtn,
        )
        logout.grid(row=8, column=0, padx=20, pady=20, sticky="s")
    
    def mng_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()

        dashboard = ctk.CTkButton(self.navbar,
            command = self.open_admindash,
            text="Admin View", **btnConfig)
        dashboard.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        payments = ctk.CTkButton(self.navbar, 
            command=lambda: None,
            text="Payments", **btnConfig)
        payments.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(self.navbar, 
            command=self.open_complaints,
            text="Complaints", **btnConfig)
        complaints.grid(row = 5, column = 0, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(self.navbar, 
            command=self.open_repairs,
            text="Repairs", **btnConfig)
        repairs.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "ew")

        reports = ctk.CTkButton(self.navbar, 
            command=lambda: None,
            text="Reports", **btnConfig)
        reports.grid(row = 7, column = 0, padx = 20, pady = 20, sticky = "ew")
        
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

    def open_maintenance_dashboard(self):
        self._invoke_controller(
            "show_dashboard",
            "open_maintenance_dashboard",
            "show_maintenance_dashboard",
        )

    def open_repairs(self):
        self._invoke_controller(
            "show_repairs",
            "open_repairs",
            "open_repairs_page",
        )

    def open_complaints(self):
        self._invoke_controller(
            "show_complaints",
            "open_complaints",
            "open_complaints_page",
        )
    
    def open_admindash(self): 
        self._invoke_controller(
            "show_admin_dashboard",
            "open_admindash",
            "show_dashboard",
        )

    def open_settings(self):
        if self._invoke_controller(
            "show_settings",
            "open_settings",
        ):
            return

        messagebox.showinfo("Settings", "Settings are not available yet.")
    
    def logoutbtn(self):
        self._invoke_controller("logout", "show_login")