import customtkinter as ctk
from tkinter import font, ttk
from gui.theme import *
from datetime import datetime
from models.front_desk import FrontDesk
from gui import page_assign_apartment
import gui.navbar as nav
from gui import page_complaints
from gui import page_repairs
import models.user_session as user_session

class FrontDeskGUI(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND)

        self.controller = controller

        self.backend = FrontDesk()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = nav.navbar(self, parent)
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        self._create_header()
        self._create_scrollFrameable_area()

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=TITLE, height=80, corner_radius=0)
        header.grid(row=0, column=1, sticky="ew", pady=(0,20))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(header, text="Front Desk", font=TITLE_FONT,
                    text_color=PRIMARY).grid(row=0, column=0, pady=20, padx=30, sticky="w")
        refresh_btn = ctk.CTkButton(header, text="↻ Refresh",
            fg_color=PRIMARY, hover_color=PRIMARY_DARK, text_color="white", 
            width=100, corner_radius=8, command= self.refresh)
        refresh_btn.grid(row=0, column=1, pady=20, padx=30, sticky="e")

    def _create_scrollFrameable_area(self):

        self.scrollFrame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND,
                                    scrollbar_button_color=PRIMARY,
                                    scrollbar_button_hover_color=PRIMARY_DARK)
        self.scrollFrame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.scrollFrame.grid_columnconfigure(0, weight=1)

        self.Register_tenant()
        self.View_tenants()
        self.Search_tenants()
        self.QuickActions()

    def Register_tenant(self):

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color = SURFACE,
            corner_radius = 12
        )
        card.grid(row=0, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text="Tenant Registration",
            font = HEADING_FONT,
            text_color = PRIMARY
        ).grid(sticky="w", padx=15, pady=(15, 5))

        def make_row(label, row):
            ctk.CTkLabel(card, text=label, text_color=TEXT_PRIMARY, font=BODY_FONT, fg_color=SURFACE).grid(row=row, column=0, sticky="w", pady=5, padx=5)
            entry = ctk.CTkEntry(card, font=BODY_FONT, fg_color=SURFACE, text_color=TEXT_PRIMARY)
            entry.grid(row=row, column=1, sticky="ew", pady=5, padx=5)
            return entry

        self.entry_name = make_row("Full Name:", 1)
        self.entry_phone = make_row("Phone:", 2)
        self.entry_ni = make_row("NI Number:", 3)
        self.entry_email = make_row("Email:", 4)

        ctk.CTkButton(card, text="Register Tenant", font=BODY_FONT,
                  fg_color=PRIMARY, text_color=SURFACE, hover_color=PRIMARY_LIGHT,
                  command=self.submit).grid(row=5, column=0, columnspan=2, pady=10)

    def View_tenants(self):
        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color="white",  # Make the card background white
            corner_radius=12
        )
        card.grid(row=1, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text="View Tenants",
            font=HEADING_FONT,
            text_color=PRIMARY
        ).grid(sticky="w", padx=15, pady=(15, 5))

        headers = ["ID", "Name", "Phone", "NI", "Email", "Created At", "Status"]
        tenants = self.backend.get_all_tenants()

        # Make columns expand evenly
        for i in range(len(headers)):
            card.grid_columnconfigure(i, weight=1)

        # Header row
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                card,
                text=h,
                font=BODY_FONT,
                text_color=PRIMARY,       
                fg_color=SECONDARY,     
                corner_radius=0,
                padx=5, pady=5
            ).grid(row=2, column=i, sticky="nsew")  # header at row 2

        # Data rows
        for r, tenant in enumerate(tenants, start=3):
            for c, val in enumerate(tenant.values()):
                bg_color = "white" if r % 2 == 0 else "#f2f2f2"  # alternating white/very light gray
                ctk.CTkLabel(
                    card,
                    text=val,
                    font=BODY_FONT,
                    text_color="black",
                    fg_color=bg_color,
                    corner_radius=0,
                    padx=5, pady=5
                ).grid(row=r, column=c, sticky="nsew")
        

    def Search_tenants(self):

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color = SURFACE,
            corner_radius = 12
        )
        card.grid(row=2, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text = "Search Tenants",
            font = HEADING_FONT,
            text_color = PRIMARY
        ).grid(sticky="w", padx=15, pady=(15, 5))
            
        ctk.CTkLabel(card, text="Search by Name:", font=BODY_FONT, text_color=PRIMARY, bg_color=SURFACE).grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.search_entry = ctk.CTkEntry(card, font=BODY_FONT, bg_color=SECONDARY, text_color=TEXT_PRIMARY, fg_color=SURFACE)
        self.search_entry.grid(row=3, column=0, sticky="ew", pady=5, padx=5)

        ctk.CTkButton(card, text="Search", font=BODY_FONT, bg_color=PRIMARY_DARK, fg_color=PRIMARY,
                  command=self.search).grid(row=4, column=0, pady=10)
        
        self.result_frame = ctk.CTkFrame(card, fg_color=SURFACE)
        self.result_frame.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
    
    def search(self):
        # Clear previous results
        for w in self.result_frame.winfo_children():
            w.destroy()

        term = self.search_entry.get().strip()
        tenants = self.backend.get_all_tenants()  # make sure this matches your other code
        found = False

        for tenant in tenants:
            name = tenant.get("fullName", "")  # adjust key to your dict
            email = tenant.get("Email", "")
            phone = tenant.get("Phone", "")

            if term in name:
                ctk.CTkLabel(
                    self.result_frame,
                    text=f"{name} — {phone} — {email}",
                    font=BODY_FONT,
                    text_color="black",   # or TEXT_PRIMARY
                    fg_color="white"      # or SURFACE if you want dark bg
                ).grid(sticky="w", pady=2)
                found = True

            if not found:
                ctk.CTkLabel(
                self.result_frame,
                text="No tenants found.",
                font=BODY_FONT,
                text_color="black",
                fg_color="white"
            ).grid(sticky="w", pady=2)
            
    def submit(self):
            name = self.entry_name.get().strip()
            phone = self.entry_phone.get().strip()
            ni = self.entry_ni.get().strip()
            email = self.entry_email.get().strip()
            try:
                self.backend.register_tenant(name, phone, ni, email)
                messagebox.showinfo("Success", "Tenant registered")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def QuickActions(self):

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color=SURFACE,
            corner_radius=12
        )
        card.grid(row=5, column = 0, sticky='ew', pady=10)

        ctk.CTkLabel(
            card,
            text = "Quick Actions",
            font= HEADING_FONT,
            text_color=PRIMARY
        ).pack(anchor="w", padx=15,pady=(15,10))

        btnFrame = ctk.CTkFrame(card, fg_color="transparent")
        btnFrame.pack(padx=15, pady=10)

        ctk.CTkButton(
            btnFrame,
            text = "Assign Apartment",
            fg_color=PRIMARY,
            command = self.open_assignApt
        ).grid(row=0,column=2,padx=10)

        ctk.CTkButton(
            btnFrame,
            text = "Complaints",
            fg_color=PRIMARY,
            command = self.open_complaints
        ).grid(row=0,column=1,padx=10)

        ctk.CTkButton(
            btnFrame,
            text = "Repairs",
            fg_color=PRIMARY,
            command = self.open_repairs
        ).grid(row=0,column=0,padx=10)

    def refresh(self):
        for widget in self.scrollFrame.winfo_children():
            widget.destroy()

        self.Register_tenant()
        self.View_tenants()
        self.Search_tenants()
        self.QuickActions()

        print("Dashboard refreshed at:", datetime.now().strftime("%H:%M:%S"))

    
    def open_assignApt(self):
        self.controller.clear_page()
        self.controller.current_page = page_assign_apartment.AssignApartmentPage(self.controller,self.controller, self.backend)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")
    
    def open_complaints(self):
        self.controller.clear_page()
        self.controller.current_page = page_complaints.ComplaintsPage(self.controller,self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def open_repairs(self):
        self.controller.clear_page()
        self.controller.current_page = page_repairs.RepairsPage(self.controller,self.controller)
        self.controller.current_page.grid(row=0, column=0, sticky="nsew")

    def clear_page(self):
        for widget in self.container.winfo_children():
            widget.destroy()