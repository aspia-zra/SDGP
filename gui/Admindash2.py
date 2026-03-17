import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import theme
from . import NavBar


class admindashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=theme.BACKGROUND)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = NavBar.navbar(self, parent)
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        self._create_header()
        self._create_scrollFrameable_area()

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=theme.SURFACE, height=80, corner_radius=0)
        header.grid(row=0, column=1, sticky="ew", pady=(0,20))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(header, text="Admin Dashboard", font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).grid(row=0, column=0, pady=20, padx=30, sticky="w")
        refresh_btn = ctk.CTkButton(header, text="↻ Refresh",
                                     fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_DARK,
                                     text_color="white", width=100, corner_radius=8)
        refresh_btn.grid(row=0, column=1, pady=20, padx=30, sticky="e")

    def _create_scrollFrameable_area(self):

        self.scrollFrame = ctk.CTkScrollableFrame(self, fg_color=theme.BACKGROUND,
                                    scrollbar_button_color=theme.PRIMARY,
                                    scrollbar_button_hover_color=theme.PRIMARY_DARK)
        self.scrollFrame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.scrollFrame.grid_columnconfigure(0, weight=1)

        self.manageStaffCard()
        self.manageAptCard()
        self.graphsCard()
        self.quickActionsCard()

    def manageStaffCard(self):

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color = theme.SURFACE,
            corner_radius = 12
        )
        card.grid(row=0, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text="Staff Management",
            font = theme.HEADING_FONT,
            text_color = theme.PRIMARY
        ).pack(anchor="w", padx=15, pady=(15, 5))

        filterFrame = ctk.CTkFrame(card, fg_color=theme.BACKGROUND)
        filterFrame.pack(fill="x", padx=15, pady=10)
        filterFrame.grid_columnconfigure(1, weight=1)

        ctk.CTkEntry( # Will only work by name
            filterFrame, 
            placeholder_text = "Search Staff..."
        ).grid(row=0, column=0, padx=5, pady=5)

        ctk.CTkComboBox( # Filter to roles
            filterFrame,
            values = ["All Roles", "Front-desk Staff", "Maintenance", "Finance"]
        ).grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkButton( # Connect to hidden page (like dropdowns) reveals fill-in sections with a submit button.
            filterFrame,
            text = "Add Staff",
            fg_color = theme.PRIMARY,
            hover_color = theme.PRIMARY_DARK
        ).grid(row=0, column=2, padx=5)

        # Table of staff details    
        tableColumns = ("ID", "Full Name", "Phone", "Email", "Role", "Location")
        staffTable = ttk.Treeview(card, columns=tableColumns, show="headings", height=8)

        for column in tableColumns:
            staffTable.heading(column, text=column)
            staffTable.column(column, anchor="center", width=120)
        staffTable.pack(fill="both", expand=True, padx=15, pady=10)

        dummydata = [ # Fill table with dummy data for now
            (1, "John Doe", "07000000000", "john@email.com", "Finance", "Bristol"),
            (2, "John Doe", "07000000000", "john@email.com", "Finance", "Bristol"),
            (3, "John Doe", "07000000000", "john@email.com", "Finance", "Bristol"),
        ]

        for dummy in dummydata:
            staffTable.insert("", "end", values=dummy)

    def manageAptCard(self): # Will cover both the manage apt and display leases

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color = theme.SURFACE,
            corner_radius = 12
        )
        card.grid(row=1, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text = "Apartment Management",
            font = theme.HEADING_FONT,
            text_color = theme.PRIMARY
        ).pack(anchor="w", padx=15, pady=(15, 5))

        filterFrame = ctk.CTkFrame(card, fg_color=theme.BACKGROUND)
        filterFrame.pack(fill="x", padx=15, pady=10)
        filterFrame.grid_columnconfigure(1, weight=1)

        ctk.CTkEntry( # Will only works for apt number
            filterFrame,
            placeholder_text = "Search Apartment..."
        ).grid(row=0, column=0, padx=5)

        ctk.CTkComboBox(
            filterFrame,
            values = ["All Cities", "Bristol", "Cardiff", "London", "Manchester"]
        ).grid(row=0, column=1, padx=5)

        ctk.CTkComboBox(
            filterFrame,
            values = ["All Status", "Occupied", "Available"]
        ).grid(row=0, column=2, padx=5)

        # Same as staff details but for apartments
        tableColumns = ("Apartment", "City", "Tenant",
            "Lease Start", "Lease End", "Rent", "Status")
        aptTable = ttk.Treeview(card, columns=tableColumns, show="headings", height=8)

        for column in tableColumns:
            aptTable.heading(column, text=column)
            aptTable.column(column, anchor="center", width=120)
        aptTable.pack(fill="both", expand=True, padx=15, pady=10)

        dummydata = [
            ("A101", "Bristol", "John Doe", "2025-01-01", "2027-01-01", "£900", "Occupied"),
            ("A102", "Bristol", "John Doe", "2023-01-01", "2024-01-01", "£950", "Occupied"),
            ("A103", "Bristol", "-", "-", "-", "£850", "Available"),
        ]

        for dummy in dummydata:
            aptTable.insert("", "end", values=dummy)

    def graphsCard(self):

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color = theme.SURFACE,
            corner_radius = 12
        )
        card.grid(row=2, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text = "Payment Graphs",
            font = theme.HEADING_FONT,
            text_color = theme.PRIMARY
        ).pack(anchor="w", padx=15, pady=(15, 5))

        aptSelect = ctk.CTkComboBox( # Links to apt card for selection?
            card,
            values = ["Apt A101", "Apt A102", "Apt A103"] # Maybe a list of all available apt?
        ) # Create for loop: Apt {aptnumber} to display all apts at relevant location
        aptSelect.pack(padx=15, pady=10, anchor="w")

        # Fake data but will eventually be relevant to apt selected
        months = ["Jan", "Feb", "Mar", "Apr", "May"]
        payments = [900, 900, 0, 900, 900]

        fig, ax = plt.subplots(figsize=(5, 2))
        ax.plot(months, payments)
        ax.set_title("Tenant Payment History")
        ax.set_ylabel("£")

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=15, pady=10)

    def quickActionsCard(self):

        card = ctk.CTkFrame(
            self.scrollFrame,
            fg_color = theme.SURFACE,
            corner_radius = 12
        )
        card.grid(row=3, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text = "Quick Actions",
            font = theme.HEADING_FONT,
            text_color = theme.PRIMARY
        ).pack(anchor="w", padx=15, pady=(15, 10))

        btnFrame = ctk.CTkFrame(card, fg_color="transparent")
        btnFrame.pack(padx=15, pady=10)

        ctk.CTkButton(
            btnFrame,
            text = "Add Apartment",
            fg_color = theme.PRIMARY
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btnFrame,
            text = "Create Lease",
            fg_color = theme.PRIMARY
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            btnFrame,
            text = "Generate Report",
            fg_color = theme.PRIMARY
        ).grid(row=0, column=2, padx=10)