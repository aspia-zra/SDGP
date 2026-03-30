import customtkinter as ctk
from tkinter import messagebox
from gui.navbar import navbar
from db.dbconnect import *
from gui.theme import *
from gui.updatedfrontdesk import FrontDeskGUI
from models.front_desk import FrontDesk
from gui.page_login import LoginPage
import models.user_session as user_sessions


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Front Desk Dashboard")
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.frontdesk_model = FrontDesk()
        

        self.current_page = None

        self.show_login()

    def show_login(self):
        self.clear_page()
        self.current_page = LoginPage(self, self.show_dashboard)
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()
        
    def show_frontdesk(self):
        self.clear_page()
        self.current_page = FrontDeskGUI(self, self)
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self, user):
        if user_sessions.user_type == "frontdesk":
            self.clear_page()
            self.current_page = self.show_frontdesk()
            self.current_page.grid(row=0, column=0, sticky="nsew")
        else:
            self.clear_page()
            label = ctk.CTkLabel(self, text="Hello")
            label.grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
