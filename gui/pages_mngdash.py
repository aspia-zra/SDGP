# trying to make this OOP for the class diagram

# need the form error validation
# need to complete backend
# need to connect to mysql on my laptop

import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from . import theme
from gui import nav as NavBar
from models.mngdash import mngBE


class mngdashboard(ctk.CTkFrame): # i need to make sure im calling the correct navbar

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
        ctk.CTkLabel(header, text="Management Dashboard", font=theme.TITLE_FONT,
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

        self.manageAptCard()
        
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
            placeholder_text = "Search by Apartment Number..."
        ).grid(row=0, column=0, padx=5)

        ctk.CTkComboBox(
            filterFrame,
            values = ["All Cities", "Bristol", "Cardiff", "London", "Manchester"]
        ).grid(row=0, column=1, padx=5)

        ctk.CTkComboBox(
            filterFrame,
            values = ["All Status", "Occupied", "Available"]
        ).grid(row=0, column=3, padx=5)

        ctk.CTkButton(
            filterFrame,
            text="Add new apartment",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            command=self.toggle_add_apartment
        ).grid(row=0, column=3, padx=5)
# hidden form
        self.addAptForm = ctk.CTkFrame(card, fg_color=theme.BACKGROUND)

        self.apt_number_entry = ctk.CTkEntry(self.addAptForm, placeholder_text="Apartment Number")
        self.apt_number_entry.grid(row=0, column=0, padx=5, pady=5)

        self.city_entry = ctk.CTkEntry(self.addAptForm, placeholder_text="City")
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        self.rent_entry = ctk.CTkEntry(self.addAptForm, placeholder_text="Rent (£)")
        self.rent_entry.grid(row=1, column=0, padx=5, pady=5)

        self.status_combo = ctk.CTkComboBox(self.addAptForm, values=["Available", "Occupied"])
        self.status_combo.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(
            self.addAptForm,
            text="Submit",
            command=self.submit_apartment
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # hide initially
        self.addAptForm.pack_forget()
# tables to display intially
        tableColumns = ("Apartment no.", "City", "Monthly Rent",
            "Status", "Lease End")

        self.aptTable = ttk.Treeview(card, columns=tableColumns, show="headings", height=8)

        for column in tableColumns:
            self.aptTable.heading(column, text=column)
            self.aptTable.column(column, anchor="center", width=120)

        self.aptTable.pack(fill="both", expand=True, padx=15, pady=10)

        self.load_table_data()
            
            #button to expand and add a new apartment
    def toggle_add_apartment(self):
        if self.addAptForm.winfo_ismapped():
            self.addAptForm.pack_forget()
        else:
            self.addAptForm.pack(fill="x", padx=15, pady=10)


    def submit_apartment(self): # click submit and get inputted values 
        #later add form validation for city etc and filled in fields
        apt = self.apt_number_entry.get()
        city = self.city_entry.get()
        rent = self.rent_entry.get()
        status = self.status_combo.get()

        new_row = (apt, city, "-", "-", f"£{rent}", status, "-")

        self.aptTable.insert("", "end", values=new_row)

# then send that data to backend:

# then refresh and reload the data

        # clear fields
        self.apt_number_entry.delete(0, "end")
        self.city_entry.delete(0, "end")
        self.rent_entry.delete(0, "end")
        self.status_combo.set("")

        # hide
        self.addAptForm.pack_forget()

    def load_table_data(self):
    #     # clear table first
        for row in self.aptTable.get_children():
             self.aptTable.delete(row)
        data = mngBE.getAptData() # from BE
        for row in data: # now put data in treeview
            apt_number = row[0]
            city = row[1] 
            monthly_rent = f"£{row[2]}"
            status = row[3]
            end_date = row[4] if row[4] else "-"
            
            self.aptTable.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
