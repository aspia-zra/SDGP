import customtkinter as ctk
from db import db_connection
from models import user_session
from gui import NavBar


class TenantDashboard(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)

        self.main = main
        self.grid(row=0, column=0, sticky="nsew")

        # Configure layout (same as settings)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main content
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR =================
        self.nav = NavBar.navbar(self, self.main)
        self.nav.grid(row=0, column=0, sticky="ns")

        # ================= MAIN CONTENT =================
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content.grid_columnconfigure((0, 1), weight=1)
        self.content.grid_rowconfigure((0, 1), weight=1)

        self.load_data()

    def refresh_dashboard(self):
        """Reload dashboard content"""
        for widget in self.content.winfo_children():
            widget.destroy()
        self.load_data()

    def load_data(self):
        user_id = user_session.current_user_id

        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        # ================= USER INFO =================
        cursor.execute("""
            SELECT fullName, Email, Phone
            FROM UserTbl
            WHERE userID = %s
        """, (user_id,))
        user = cursor.fetchone()

        info_card = ctk.CTkFrame(self.content)
        info_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(info_card, text="Your Details", font=("Arial", 16, "bold")).pack(pady=10)

        if user:
            ctk.CTkLabel(info_card, text=f"Name: {user['fullName']}").pack(anchor="w", padx=10)
            ctk.CTkLabel(info_card, text=f"Email: {user['Email']}").pack(anchor="w", padx=10)
            ctk.CTkLabel(info_card, text=f"Phone: {user['Phone']}").pack(anchor="w", padx=10)

        # ================= APARTMENT INFO =================
        cursor.execute("""
            SELECT a.apartmentNumber, a.Type, a.monthlyRent
            FROM Tenant t
            JOIN LeaseAgreement l ON t.tenantID = l.tenantID
            JOIN Apartment a ON l.apartmentID = a.apartmentID
            WHERE t.userID = %s AND l.Status = 'active'
        """, (user_id,))
        apartment = cursor.fetchone()

        apt_card = ctk.CTkFrame(self.content)
        apt_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(apt_card, text="Your Apartment", font=("Arial", 16, "bold")).pack(pady=10)

        if apartment:
            ctk.CTkLabel(apt_card, text=f"Apartment: {apartment['apartmentNumber']}").pack(anchor="w", padx=10)
            ctk.CTkLabel(apt_card, text=f"Type: {apartment['Type']}").pack(anchor="w", padx=10)
            ctk.CTkLabel(apt_card, text=f"Rent: £{apartment['monthlyRent']}").pack(anchor="w", padx=10)
        else:
            ctk.CTkLabel(apt_card, text="No active lease").pack()

        # ================= INVOICES =================
        cursor.execute("""
            SELECT i.Amount, i.dueDate, i.Status
            FROM Tenant t
            JOIN LeaseAgreement l ON t.tenantID = l.tenantID
            JOIN Invoice i ON l.leaseID = i.leaseID
            WHERE t.userID = %s
            ORDER BY i.dueDate DESC
        """, (user_id,))
        invoices = cursor.fetchall()

        pay_card = ctk.CTkFrame(self.content)
        pay_card.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(pay_card, text="Your Payments", font=("Arial", 16, "bold")).pack(pady=10)

        if invoices:
            for inv in invoices:
                text = f"£{inv['Amount']} | Due: {inv['dueDate']} | Status: {inv['Status']}"
                ctk.CTkLabel(pay_card, text=text).pack(anchor="w", padx=10)
        else:
            ctk.CTkLabel(pay_card, text="No invoices found").pack()

        conn.close()