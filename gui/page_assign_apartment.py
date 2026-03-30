import customtkinter as ctk
from tkinter import messagebox
from gui.theme import *
from models.front_desk import FrontDesk
import gui.navbar as nav


class AssignApartmentPage(ctk.CTkFrame):
    def __init__(self, parent, controller, frontdesk_model):
        super().__init__(parent, fg_color=BACKGROUND)
        self.controller = controller
        self.model = frontdesk_model

        self.nav = nav.navbar(self, parent)
        self.nav.grid(row=0, rowspan=4, column=0, sticky="ns")

        # ===== GRID SETUP =====
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main content

        # ===== MAIN CONTENT AREA =====
        self.main_frame = ctk.CTkFrame(self, fg_color=BACKGROUND)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # ===== TITLE =====
        ctk.CTkLabel(
            self.main_frame,
            text="Assign Apartment",
            font=("Arial", 28, "bold"),
            text_color=PRIMARY
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        # ===== CARD =====
        card = ctk.CTkFrame(
            self.main_frame,
            fg_color=SURFACE,
            corner_radius=12,
            width=700,
            height=350
        )
        card.grid(row=1, column=0, sticky="n", padx=10, pady=10)
        card.grid_propagate(False)

        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)

        # ===== TENANT DROPDOWN =====
        ctk.CTkLabel(
            card,
            text="Select Tenant:",
            text_color=TEXT_PRIMARY,
            font=("Arial", 16)
        ).grid(row=0, column=0, pady=20, padx=20, sticky="w")

        self.tenant_var = ctk.StringVar()
        self.tenant_dropdown = ctk.CTkOptionMenu(
            card,
            variable=self.tenant_var,
            values=[""],
            font=("Arial", 16),
            width=320,
            height=40,
            fg_color=BACKGROUND,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_DARK,
            text_color=TEXT_PRIMARY,
            dropdown_fg_color=BACKGROUND,
            dropdown_text_color=TEXT_PRIMARY
        )
        self.tenant_dropdown.grid(row=0, column=1, pady=20, padx=20, sticky="ew")

        # ===== APARTMENT DROPDOWN =====
        ctk.CTkLabel(
            card,
            text="Select Apartment:",
            text_color=TEXT_PRIMARY,
            font=("Arial", 16)
        ).grid(row=1, column=0, pady=20, padx=20, sticky="w")

        self.apartment_var = ctk.StringVar()
        self.apartment_dropdown = ctk.CTkOptionMenu(
            card,
            variable=self.apartment_var,
            values=[""],
            font=("Arial", 16),
            width=320,
            height=40,
            fg_color=BACKGROUND,
            button_color=PRIMARY,
            button_hover_color=PRIMARY_DARK,
            text_color=TEXT_PRIMARY,
            dropdown_fg_color=BACKGROUND,
            dropdown_text_color=TEXT_PRIMARY
        )
        self.apartment_dropdown.grid(row=1, column=1, pady=20, padx=20, sticky="ew")

        # ===== BUTTON =====
        ctk.CTkButton(
            card,
            text="Assign Apartment",
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            text_color="white",
            font=("Arial", 16, "bold"),
            width=220,
            height=45,
            command=self.assign_apartment
        ).grid(row=2, column=0, columnspan=2, pady=30)

        self.populate_dropdowns()

    # ===== POPULATE DROPDOWNS =====
    def populate_dropdowns(self):
        try:
            tenants = self.model.get_all_tenants()
            tenant_names = [f"{t['tenantID']}: {t['fullName']}" for t in tenants]

            if tenant_names:
                self.tenant_dropdown.configure(values=tenant_names)
                self.tenant_var.set(tenant_names[0])
            else:
                self.tenant_dropdown.configure(values=["No tenants found"])
                self.tenant_var.set("No tenants found")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load tenants: {e}")

        try:
            apartments = self.model.get_all_apartments()
            apartment_list = [str(a) for a in apartments]

            if apartment_list:
                self.apartment_dropdown.configure(values=apartment_list)
                self.apartment_var.set(apartment_list[0])
            else:
                self.apartment_dropdown.configure(values=["No apartments found"])
                self.apartment_var.set("No apartments found")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load apartments: {e}")

    # ===== ASSIGN FUNCTION =====
    def assign_apartment(self):
        tenant_value = self.tenant_var.get()
        apartment_id = self.apartment_var.get()

        if not tenant_value or tenant_value == "No tenants found":
            messagebox.showerror("Error", "Please select a tenant.")
            return

        if not apartment_id or apartment_id == "No apartments found":
            messagebox.showerror("Error", "Please select an apartment.")
            return

        tenant_id = tenant_value.split(":")[0].strip()

        try:
            self.model.assign_apartment(tenant_id, apartment_id)
            messagebox.showinfo("Success", f"{apartment_id} assigned to tenant {tenant_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))