import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

from gui.loginpage import LoginPage
from gui.tenant_dashboard import TenantDashboard
import models.user_session as user_session  # ✅ IMPORTANT


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Paragon Apartment System")
        self.geometry("1000x700")
        self.minsize(800, 600)

        self.current_page = None
        self.show_login()

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()

    def show_login(self):
        self.clear_page()
        self.current_page = LoginPage(self, self.show_dashboard)
        self.current_page.pack(fill="both", expand=True)

    # ================= DASHBOARD =================
    def show_dashboard(self, user, user_type):
        self.clear_page()

        # ✅ CRITICAL FIX — SAVE SESSION
        user_session.user_sessions(user)

        # TENANT DASHBOARD
        if user_type == "tenant":
            self.current_page = TenantDashboard(self)
            self.current_page.pack(fill="both", expand=True)
            return

        # STAFF DASHBOARD
        dashboard = ctk.CTkFrame(self)
        dashboard.pack(fill="both", expand=True)

        welcome_text = "Welcome " + user["fullName"] + " - " + user["Role"]

        ctk.CTkLabel(
            dashboard,
            text=welcome_text,
            font=("Arial", 22)
        ).pack(pady=100)

        self.current_page = dashboard

    # ================= PAYMENTS PAGE NAV =================
    def show_payments(self):
        self.clear_page()

        page = ctk.CTkFrame(self)
        page.pack(fill="both", expand=True)

        ctk.CTkLabel(
            page,
            text="Payments Page (connect yours here)",
            font=("Arial", 20)
        ).pack(pady=100)

        ctk.CTkButton(
            page,
            text="Back",
            command=lambda: self.show_login()
        ).pack()

        self.current_page = page


if __name__ == "__main__":
    app = App()
    app.mainloop()