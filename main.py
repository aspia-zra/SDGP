import customtkinter as ctk
from gui.loginpage import LoginPage
from gui.finance_view import FinanceView
from gui.reports_view import ReportsView
from gui.payment_page import PaymentPage
import models.user_session as user_session
from gui import theme


class PAMSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Paragon Apartment Management System")
        self.geometry("1200x700")
        ctk.set_appearance_mode("light")
        self.configure(fg_color=theme.BACKGROUND)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.current_page = None
        self.show_login()

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()

    def show_login(self):
        self.clear_page()
        self.current_page = LoginPage(self, self.show_dashboard)
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self, user=None):
        role = user_session.user_type

        if role == "finance":
            self.clear_page()
            self.navbar_mode = role
            self.current_page = FinanceView(self, self)
            self.current_page.grid(row=0, column=0, sticky="nsew")
        else:
            self.clear_page()
            label = ctk.CTkLabel(self, text=f"Role '{role}' not set up yet")
            label.grid(row=0, column=0)


if __name__ == "__main__":
    app = PAMSApp()
    app.mainloop()