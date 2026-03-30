import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import GUI.theme as theme
from datetime import datetime
from . import nav
from Models.admindashBE import adminBE


class admindashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=theme.BACKGROUND)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = nav.navbar(self, parent)
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        self._create_header()
        self._create_scrollFrameable_area()

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color=theme.TITLE, height=80, corner_radius=0)
        header.grid(row=0, column=1, sticky="ew", pady=(0,20))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(header, text="Admin View", font=theme.TITLE_FONT,
                    text_color=theme.PRIMARY).grid(row=0, column=0, pady=20, padx=30, sticky="w")
        refresh_btn = ctk.CTkButton(header, text="↻ Refresh",
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_DARK, text_color="white", 
            width=100, corner_radius=8, command= self.refresh)
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

        self.editStaffBtn = ctk.CTkButton( # Filter to roles
            filterFrame,
            text = "Edit",
            fg_color= theme.PRIMARY,
            hover_color= theme.PRIMARY_LIGHT,
            command = self.editStaffdrop
        )
        self.editStaffBtn.grid(row=0, column=1, padx=5, pady=5)
        
        self.addStaffBtn = ctk.CTkButton( # Connect to hidden page (like dropdowns) reveals fill-in sections with a submit button.
            filterFrame,
            text = "Add Staff",
            fg_color = theme.PRIMARY,
            hover_color = theme.PRIMARY_LIGHT,
            command = self.addStaffdrop
        )
        self.addStaffBtn.grid(row=0, column=2, padx=5)

        tableFrame = ctk.CTkFrame(card, fg_color="transparent")
        tableFrame.pack(fill="both", expand=True, padx=15, pady=10)
        tableFrame.grid_rowconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(0, weight=1)
        tableFrame.grid_columnconfigure(1, weight=0)

        # Table of staff details    - Scroll bar (revisit)
        tableColumns = ("ID", "Full Name", "Phone", "Email", "Role", "Location")
        self.staffTable = ttk.Treeview(tableFrame, columns=tableColumns, show="headings", height=8)

        scrollbar = ttk.Scrollbar(tableFrame, orient="vertical", command=self.staffTable.yview)
        self.staffTable.configure(yscrollcommand=scrollbar.set)

        self.staffTable.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for column in tableColumns:
            self.staffTable.heading(column, text=column)
            self.staffTable.column(column, anchor="center", width=120)

        self.staffTable.bind('<<Saved Select>>', self.onSelect)

        staffData = adminBE.getStaffData()

        for staff in staffData:
            self.staffTable.insert("", "end", values=staff)

        tableFrame.update_idletasks()

        # When add staff is pressed:
        self.addStaffVisible = False

        self.addStaffFrame = ctk.CTkFrame(card, fg_color=theme.BACKGROUND)
        self.addStaffFrame.pack(fill="x", padx=15, pady=10)
        self.addStaffFrame.pack_forget() 

        self.addStaffFrame.grid_columnconfigure(0, weight=1)
        self.addStaffFrame.grid_columnconfigure(1, weight=1)
        self.addStaffFrame.grid_columnconfigure(2, weight=0)

        self.addNameEntry = ctk.CTkEntry(self.addStaffFrame, placeholder_text="Full Name")
        self.addNameEntry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.addPhoneEntry = ctk.CTkEntry(self.addStaffFrame, placeholder_text="Phone")
        self.addPhoneEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.addEmailEntry = ctk.CTkEntry(self.addStaffFrame, placeholder_text="Email")
        self.addEmailEntry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.addPassEntry = ctk.CTkEntry(self.addStaffFrame, placeholder_text="Password", show="*")
        self.addPassEntry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.addRoleEntry = ctk.CTkEntry(self.addStaffFrame, placeholder_text="Role")
        self.addRoleEntry.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        ctk.CTkButton( 
            self.addStaffFrame,
            text = "Submit",
            fg_color = theme.PRIMARY,
            hover_color = theme.PRIMARY_LIGHT,
            command= self.submitStaff
        ).grid(row=1, column=2, padx=5)

        # When edit staff is pushed:
        self.editStaffVisible = False
        self.selectStaffID = None

        self.editStaffFrame = ctk.CTkFrame(card, fg_color=theme.BACKGROUND)
        self.editStaffFrame.pack(fill="x", padx=15, pady=10)
        self.editStaffFrame.pack_forget() 

        self.editStaffFrame.grid_columnconfigure(0, weight=1)
        self.editStaffFrame.grid_columnconfigure(1, weight=1)
        self.editStaffFrame.grid_columnconfigure(2, weight=0)

        self.editNameEntry = ctk.CTkEntry(self.editStaffFrame)
        self.editNameEntry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.editPhoneEntry = ctk.CTkEntry(self.editStaffFrame)
        self.editPhoneEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.editEmailEntry = ctk.CTkEntry(self.editStaffFrame)
        self.editEmailEntry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.editRoleEntry = ctk.CTkEntry(self.editStaffFrame)
        self.editRoleEntry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkButton( 
            self.editStaffFrame,
            text = "Update",
            fg_color = theme.PRIMARY,
            hover_color = theme.PRIMARY_LIGHT,
            command= self.updateStaff
        ).grid(row=0, column=4, padx=5)

        self.labelFrame = ctk.CTkFrame(card, fg_color=theme.TITLE)
        self.labelFrame.pack(fill="x", padx=15, pady=10)
        self.labelFrame.pack_forget() 
        self.labelBanner = ctk.CTkLabel(self.labelFrame, text="", text_color=theme.SURFACE)
        self.labelBanner.pack(fill="x", padx=5, pady=5)


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
        aptTable = ttk.Treeview(card, columns=tableColumns, show="headings")

        for column in tableColumns:
            aptTable.heading(column, text=column)
            aptTable.column(column, anchor="center", width=120)
        aptTable.pack(fill="both", expand=True, padx=15, pady=10)

        aptData = adminBE.getAptData()

        for apt in aptData:
            aptNumber, City, Tenant, startDate, endDate, Rent, Status = apt
            Tenant = Tenant if Tenant else "-"
            startDate = startDate if startDate else "-"
            endDate = endDate if endDate else "-"
            aptTable.insert("", "end", values=(aptNumber, City, Tenant, 
                                               startDate, endDate, Rent, Status))

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

        aptList = adminBE.getAptList()
        aptDrop = {f"Apt {apt[0]}": apt[0] for apt in aptList}

        dropdown = ["Select"] + list(aptDrop.keys())
        self.aptSelect = ctk.CTkComboBox( 
            card,
            values = dropdown, # Track which selected
            command=self.selectedApt
        ) 
        self.aptSelect.pack(padx=15, pady=10, anchor="w")

        # Plot my bar chart
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=card)
        self.canvas.get_tk_widget().pack(padx=15, pady=10)

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
            fg_color = theme.PRIMARY,
            command = self.open_assignApt
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

    def refresh(self):
        for widget in self.scrollFrame.winfo_children():
            widget.destroy()

        self.manageStaffCard()
        self.manageAptCard()
        self.graphsCard()
        self.quickActionsCard()

        print("Dashboard refreshed at:", datetime.now().strftime("%H:%M:%S"))

    def selectedApt(self, apt):
        self.ax.clear()
        if apt == "Select": 
            self.ax.text(0.5, 0.5, "Select an Apartment", 
                    ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
            
        actual_apt = apt.replace("Apt ", "")
        tenantData, neighbour1, neighbour2 = adminBE.tenantGraphs(actual_apt)

        if not tenantData:
            self.ax.text(0.5, 0.5, "No payment data available for this apartment", 
                    ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return

        month = sorted(list({d[1] for d in tenantData}))
        x = range(len(month))

        fullName = tenantData[0][0]
        tenant_paid = [sum(d[2] for d in tenantData if d[1]==m) for m in month]
        self.ax.bar([i - 0.25 for i in x], tenant_paid, width=0.25, label=fullName)

        if neighbour1:
            NfullName = neighbour1[0][0]
            n1Paid = [sum(d[2] for d in neighbour1 if d[1]==m) for m in month]
            self.ax.bar(x, n1Paid, width=0.25, label=NfullName)
        
        if neighbour2:
            N2fullName = neighbour2[0][0]
            n2Paid = [sum(d[2] for d in neighbour2 if d[1]==m) for m in month]
            self.ax.bar([i + 0.25 for i in x], n2Paid, width=0.25, label=N2fullName)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(month, rotation=45)
        self.ax.set_ylabel("Total Payments")
        self.ax.set_title("Tenant Payments vs Neighbor/s")
        self.ax.legend()
        self.fig.tight_layout()  
        self.canvas.draw()

    def addStaffdrop(self):
        if self.addStaffVisible:
            self.addStaffBtn.configure(text="Add Staff")
            self.addStaffFrame.pack_forget()
            self.addStaffVisible = False
        else:
            self.addStaffBtn.configure(text="Close")
            self.addStaffFrame.pack(fill="x", padx=15, pady=10)
            self.addStaffVisible = True

    def submitStaff(self): # add more if statements to check entries
        fullName = self.addNameEntry.get().strip()
        Phone = self.addPhoneEntry.get().strip()
        Email = self.addEmailEntry.get().strip()
        Password = self.addPassEntry.get().strip()
        Role = self.addRoleEntry.get().strip()

        if not all([fullName, Phone, Email, Password, Role]):
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Please fill all fields.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return

        adminBE.addStaff(fullName, Phone, Email, Password, Role)
        self.labelFrame.pack(fill="x", padx=15, pady=10)
        self.labelBanner.configure(text="Success!", fg_color=theme.SUCCESS)
        self.after(3000, lambda: self.labelFrame.pack_forget())

        self.addNameEntry.delete(0, "end")
        self.addPhoneEntry.delete(0, "end")
        self.addEmailEntry.delete(0, "end")
        self.addRoleEntry.delete(0, "end")
        self.addPassEntry.delete(0, "end")

    def editStaffdrop(self):
        if self.editStaffVisible:
            self.editStaffBtn.configure(text="Edit")
            self.editStaffFrame.pack_forget()
            self.editStaffVisible = False
        else:
            self.editStaffBtn.configure(text="Close")
            self.editStaffFrame.pack(fill="x", padx=15, pady=10)
            self.editStaffVisible = True

    def onSelect(self):
        data = self.staffTable.selection()
        if not data:
            return
        for item in data:
            self.selectStaffID = item[0]


    def updateStaff(self):
        pass

