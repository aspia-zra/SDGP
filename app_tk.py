from tkinter import *
import customtkinter as ctk
from GUI.Admindash import *
from GUI.loginpage import *
import Models.user_session as user_session 
from GUI.NavBar import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Paragon Apartment System")
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.current_page = None

        self.show_login()

    def clear_page(self):
        if self.current_page != None:
            self.current_page.destroy()

    def show_login(self):
        self.clear_page()
        self.current_page = LoginPage(self, self.show_dashboard)
        self.current_page.grid(row=0, column=0, sticky="nsew")
    
    # add dashboard page based on role

    def show_dashboard(self, user):
        if user_session.user_type == "admin":
            self.clear_page()
            self.current_page = admindashboard(self)
            self.current_page.grid(row=0, column=0, sticky="nsew")
        else:
            self.clear_page()
            label = ctk.CTkLabel(self, text="Hello")
            label.grid(row=0, column=0)

if __name__ == '__main__':   
   app = App()
   app.mainloop()