<<<<<<< HEAD
from tkinter import messagebox
import customtkinter as ctk
from models import user_session
from gui import theme

BG_COLOR = theme.BACKGROUND


class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller, mode="finance"):
        super().__init__(parent, fg_color=theme.SECONDARY)
        self.controller = controller
        self.mode = mode

        self.grid(row=0, column=0, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_navbar()

    def create_navbar(self):
        mode = getattr(self.controller, "navbar_mode", self.mode)
        mode = str(mode or "").lower()

        if mode == "finance":
            self.finance_nav()
            return

        self.finance_nav()

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
            font=(theme.TITLE_FONT, 20),
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

    def finance_nav(self):
        self._reset_navbar()
        btnConfig = self._nav_button_config()
        ctk.CTkButton(self.navbar, command=self.open_financedash, text="Finance Dashboard", **btnConfig).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_reports, text="Reports", **btnConfig).grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, command=self.open_payments, text="Payments", **btnConfig).grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(self.navbar, fg_color=theme.PRIMARY, hover_color=theme.DANGER, text="Logout", command=self.logoutbtn).grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def open_financedash(self):
        from gui.finance_view import FinanceView
        self.controller.clear_page()
        self.controller.current_page = FinanceView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_reports(self):
        from gui.finance_reports_view import FinanceReportsView
        self.controller.clear_page()
        self.controller.current_page = FinanceReportsView(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_payments(self):
        from gui.payment_page import PaymentPage
        self.controller.clear_page()
        self.controller.current_page = PaymentPage(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def logoutbtn(self):
        user_session.clear()
        self.controller.show_login()
=======
from tkinter import *
import customtkinter as ctk
from models.logincode import UserTbl
from gui.theme import *
from gui.updatedfrontdesk import FrontDeskGUI
from gui.page_complaints import ComplaintsPage
from gui.page_repairs import RepairsPage
from gui.page_assign_apartment import AssignApartmentPage
from models.front_desk import FrontDesk


class navbar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SECONDARY)
        self.controller = controller
        self.model = FrontDesk()

        self.grid(row=0, column=0, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_navbar()
        
    def create_navbar(self):
        self.navbar = ctk.CTkFrame(self, fg_color="transparent")
        self.navbar.grid(row=0, column=0, sticky="ns")
        self.navbar.grid_rowconfigure(7, weight=1)
        self.navbar.grid_columnconfigure(0, weight=1)

        #TITLE
        navtitle_label = ctk.CTkLabel(
            self.navbar, 
            text="Paragon Apartments", 
            fg_color= "transparent",
            text_color=PRIMARY,
            font=(TITLE_FONT, 20))
        navtitle_label.grid(row = 0, column = 0, padx = 20, pady = (20,40), sticky="w")

        btnConfig = { # Styling for buttons here
            "fg_color": PRIMARY,
            "hover_color": PRIMARY_DARK,
            "text_color": SURFACE,
            "height": 40,
            "corner_radius": 8,
            "anchor": "w",
        }

        dashboard = ctk.CTkButton(self.navbar,
            command = self.open_frontdesk,
            text="Dashboard", **btnConfig)
        dashboard.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        complaints = ctk.CTkButton(self.navbar, command=self.open_complaints,
            text="Complaints", **btnConfig)
        complaints.grid(row = 2, column = 0, padx = 20, pady = 20, sticky = "ew")

        repairs = ctk.CTkButton(self.navbar, command=self.open_repairs,
            text="Repairs", **btnConfig)
        repairs.grid(row = 3, column = 0, padx = 20, pady = 20, sticky = "ew")

        assign_apartment = ctk.CTkButton(self.navbar, command=self.open_assign_apartment,
            text="Assign Apartment", **btnConfig)
        assign_apartment.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "ew")

        # settings_btn = ctk.CTkButton(
        #       self.navbar,
        #       command=self.open_settings,
        #       text="Settings",
        #       **btnConfig)
        # settings_btn.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        logout = ctk.CTkButton(self.navbar, 
            fg_color=PRIMARY, 
            hover_color=DANGER, 
            text="Logout", 
            command = self.logoutbtn)
        logout.grid(row = 8, column = 0, padx = 20, pady = 20, sticky = "s")
    
    def clear_page(self):
        for widget in self.winfo_children():
            # keep navbar, remove everything else
            if not isinstance(widget, navbar):
                widget.destroy()

    def open_frontdesk(self):
        self.controller.clear_page()
        self.controller.current_page = FrontDeskGUI(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def open_complaints(self):
        self.controller.clear_page()
        self.controller.current_page = ComplaintsPage(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_repairs(self):
        self.controller.clear_page()
        self.controller.current_page = RepairsPage(self.controller, self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def open_assign_apartment(self):
        self.controller.clear_page()
        self.controller.current_page = AssignApartmentPage(self.controller, self.controller, self.model)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    # def open_settings(self):
    #     self.controller.clear_page()
    #     self.controller.current_page = settings(self.controller)
    #     self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def logoutbtn(self):
        UserTbl.logout()
        self.controller.show_login()
>>>>>>> origin/Azra-management-dashboard
