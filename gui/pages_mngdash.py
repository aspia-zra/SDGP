# trying to make this OOP for the class diagram

# need the form error validation
# need to complete backend
# need to connect to mysql on my laptop
# all fields requied popup
# form text

import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from . import theme
from . import nav
from models.mngdash import mngBE


class mngdashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=theme.BACKGROUND)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = nav.navbar(self, parent)
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        self._create_header()
        self._create_scrollFrameable_area()

    def _validate_form_inputs(self):
        apt_number = self.apt_number_entry.get().strip()
        monthly_rent = self.rent_entry.get().strip()
        status = self.status_combo.get().strip()
        city = self.city_entry.get().strip()

        if not apt_number or not monthly_rent or not status or not city:
            return False, "All fields required"

        if not monthly_rent.isdigit() or int(monthly_rent) <= 500:
            return False, "Please input a valid number above £500 for the rent"

        if not apt_number.isdigit():
            return False, "Apartment number must be a number"

        existing_numbers = {str(row[0]).strip() for row in mngBE.getAptData()}
        if apt_number in existing_numbers:
            return False, "Please input an apartment number that is not already taken"

        return True, ""

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=theme.SURFACE, height=80, corner_radius=0)
        header.grid(row=0, column=1, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            header,
            text="Management Dashboard",
            font=theme.TITLE_FONT,
            text_color=theme.PRIMARY,
        ).grid(row=0, column=0, pady=20, padx=30, sticky="w")

    def _create_scrollFrameable_area(self):
        self.scrollFrame = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.BACKGROUND,
            scrollbar_button_color=theme.PRIMARY,
            scrollbar_button_hover_color=theme.PRIMARY_DARK,
        )
        self.scrollFrame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.scrollFrame.grid_columnconfigure(0, weight=1)

        self.manageAptCard()

    def _configure_table_style(self):
        style = ttk.Style(self)
        style.configure(
            "AptTable.Treeview",
            font=theme.BODY_FONT,
            rowheight=28,
            background=theme.SURFACE,
            foreground=theme.TEXT_PRIMARY,
            fieldbackground=theme.SURFACE,
            bordercolor=theme.SECONDARY,
        )
        style.configure(
            "AptTable.Treeview.Heading",
            font=theme.HEADING_FONT,
            background=theme.PRIMARY,
            foreground=theme.PRIMARY_DARK,
        )
        style.map(
            "AptTable.Treeview",
            background=[("selected", theme.PRIMARY_LIGHT)],
            foreground=[("selected", theme.TITLE)],
        )

    def manageAptCard(self):
        card = ctk.CTkFrame(self.scrollFrame, fg_color=theme.SURFACE, corner_radius=12)
        card.grid(row=1, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text="Apartment Management",
            font=theme.HEADING_FONT,
            text_color=theme.PRIMARY,
        ).pack(anchor="w", padx=15, pady=(15, 5))

        filterFrame = ctk.CTkFrame(card, fg_color=theme.BACKGROUND)
        filterFrame.pack(fill="x", padx=15, pady=10)
        filterFrame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            filterFrame,
            text="Add new apartment",
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.BACKGROUND,
            font=theme.BODY_FONT,
            command=self.toggle_add_apartment,
        ).grid(row=0, column=3, padx=5)

        self.addAptForm = ctk.CTkFrame(card, fg_color=theme.BACKGROUND, corner_radius=10)

        self.apt_number_entry = ctk.CTkEntry(
            self.addAptForm,
            placeholder_text="Apartment Number",
            font=theme.HEADING_FONT,
            fg_color=theme.SURFACE,
            text_color=theme.PRIMARY_DARK,
            border_color=theme.SECONDARY,
        )
        self.apt_number_entry.grid(row=0, column=0, padx=5, pady=5)

        self.city_entry = ctk.CTkEntry(
            self.addAptForm,
            placeholder_text="City",
            font=theme.BODY_FONT,
            fg_color=theme.SURFACE,
            text_color=theme.TEXT_PRIMARY,
            border_color=theme.SECONDARY,
        )
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        self.rent_entry = ctk.CTkEntry(
            self.addAptForm,
            placeholder_text="Rent (£)",
            font=theme.BODY_FONT,
            fg_color=theme.SURFACE,
            text_color=theme.TEXT_PRIMARY,
            border_color=theme.SECONDARY,
        )
        self.rent_entry.grid(row=1, column=0, padx=5, pady=5)

        self.status_combo = ctk.CTkComboBox(
            self.addAptForm,
            values=["Available", "Occupied"],
            font=theme.BODY_FONT,
            fg_color=theme.SURFACE,
            border_color=theme.SECONDARY,
            button_color=theme.PRIMARY,
            button_hover_color=theme.PRIMARY_DARK,
            text_color=theme.TEXT_PRIMARY,
            dropdown_fg_color=theme.SURFACE,
            dropdown_text_color=theme.TEXT_PRIMARY,
        )
        self.status_combo.grid(row=1, column=1, padx=5, pady=5)

        self.submit_button = ctk.CTkButton(
            self.addAptForm,
            text="Submit",
            font=theme.BODY_FONT,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_DARK,
            text_color=theme.TITLE,
            command=self.submit_apartment,
        )
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.addAptForm.pack_forget()

        tableColumns = ("Apartment no.", "City", "Monthly Rent", "Status", "Lease End")
        self._configure_table_style()
        self.aptTable = ttk.Treeview(card, columns=tableColumns, show="headings", height=8, style="AptTable.Treeview")

        for column in tableColumns:
            self.aptTable.heading(column, text=column)
            self.aptTable.column(column, anchor="center", width=120)

        self.aptTable.pack(fill="both", expand=True, padx=15, pady=10)

        self.status_combo.set("Available")
        self.load_table_data()

    def toggle_add_apartment(self):
        if self.addAptForm.winfo_ismapped():
            self.addAptForm.pack_forget()
        else:
            self.addAptForm.pack(fill="x", padx=15, pady=10)

    def submit_apartment(self):
        apt_number = self.apt_number_entry.get().strip()
        monthly_rent = self.rent_entry.get().strip()
        status = self.status_combo.get().strip()
        city = self.city_entry.get().strip()

        is_valid, validation_message = self._validate_form_inputs()
        if not is_valid:
            messagebox.showerror("Validation Error", validation_message)
            return

        try:
            mngBE.addApt(
                apartmentNumber=apt_number,
                monthlyRent=int(monthly_rent),
                status=status,
                city=city,
            )
            messagebox.showinfo("Success", "Apartment added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding apartment: {e}")
            return

        self.load_table_data()

        self.apt_number_entry.delete(0, "end")
        self.rent_entry.delete(0, "end")
        self.status_combo.set("Available")
        self.city_entry.delete(0, "end")

    def load_table_data(self):
        for row in self.aptTable.get_children():
            self.aptTable.delete(row)

        data = mngBE.getAptData()
        for row in data:
            self.aptTable.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))








