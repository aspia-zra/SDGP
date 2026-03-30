import customtkinter as ctk
from models.tenant_dashboardBE import get_tenant_data
from datetime import datetime
from . import theme
from .nav import navbar   


class TenantDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        self.controller = controller

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navbar = navbar(self, controller, mode="tenant")
        self.navbar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self, fg_color=theme.BACKGROUND)
        self.content.grid(row=0, column=1, sticky="nsew")

        self.content.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(
            self.content,
            text="Tenant Dashboard",
            font=(theme.TITLE_FONT, 28),
            text_color=theme.PRIMARY
        )
        title.grid(row=0, column=0, columnspan=2, pady=20)

        self.data = get_tenant_data()

        self.create_personal_card()
        self.create_apartment_card()
        self.create_lease_card()

    def create_card(self, row, column, title_text):
        frame = ctk.CTkFrame(self.content, fg_color=theme.SECONDARY, corner_radius=12)
        frame.grid(row=row, column=column, padx=20, pady=15, sticky="nsew")

        title = ctk.CTkLabel(
            frame,
            text=title_text,
            font=(theme.TITLE_FONT, 18),
            text_color=theme.PRIMARY
        )
        title.pack(pady=(10, 5))

        return frame


    def create_personal_card(self):
        frame = self.create_card(1, 0, "👤 Personal Info")

        self.add_item(frame, "Name", self.data.get("fullName"))
        self.add_item(frame, "Email", self.data.get("Email"))
        self.add_item(frame, "Phone", self.data.get("Phone"))
        self.add_item(frame, "NI Number", self.data.get("national_Insurance"))
        self.add_item(frame, "Status", self.data.get("tenantStatus"))


    def create_apartment_card(self):
        frame = self.create_card(1, 1, "🏢 Apartment")

        self.add_item(frame, "Apartment", self.data.get("apartmentNumber"))
        self.add_item(frame, "Type", self.data.get("Type"))
        self.add_item(frame, "Rent", f"£{self.data.get('monthlyRent')}")
        self.add_item(frame, "Status", self.data.get("apartmentStatus"))

        ctk.CTkLabel(frame, text="").pack()

        self.add_item(frame, "Address", self.data.get("Address"))
        self.add_item(frame, "City", self.data.get("City"))
        self.add_item(frame, "Office Phone", self.data.get("locationPhone"))

    def create_lease_card(self):
        frame = self.create_card(2, 0, "📄 Lease Info")

        self.add_item(frame, "Start Date", self.data.get("startDate"))
        self.add_item(frame, "End Date", self.data.get("endDate"))
        self.add_item(frame, "Deposit", f"£{self.data.get('depositAmount')}")
        self.add_item(frame, "Status", self.data.get("leaseStatus"))

        end_date = self.data.get("endDate")
        if end_date:
            try:
                end_date_obj = datetime.strptime(str(end_date), "%Y-%m-%d")
                days_left = (end_date_obj - datetime.now()).days

                color = "green" if days_left > 30 else "orange" if days_left > 7 else "red"

                ctk.CTkLabel(
                    frame,
                    text=f"Days Remaining: {days_left}",
                    text_color=color
                ).pack(pady=5)

            except:
                pass

    def add_item(self, parent, label, value):
        text = f"{label}: {value if value else 'N/A'}"
        ctk.CTkLabel(parent, text=text, anchor="w").pack(fill="x", padx=20, pady=2)