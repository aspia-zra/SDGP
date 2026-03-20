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

        # settings = ctk.CTkButton(self.navbar, 
        #     command = self.open_settings,
        #     text="Settings", **btnConfig)
        # settings.grid(row = 3, column = 0, padx = 20, pady = 20, sticky = "ew")

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
    #     self.controller.current_page = settings.settings(self.controller)
    #     self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def logoutbtn(self):
        UserTbl.logout()
        self.controller.show_login()