import customtkinter as ctk
from tkinter import messagebox
from gui.navbar import navbar
from db.dbconnect import Database
from gui.theme import *
from gui.updatedfrontdesk import FrontDeskGUI
from models.front_desk import FrontDesk



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Front Desk Dashboard")
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.frontdesk_model = FrontDesk()

        self.current_page = None

        self.show_frontdesk()

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()
        
    def show_frontdesk(self):
        self.clear_page()
        self.current_page = FrontDeskGUI(self, self)
        self.current_page.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
