import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from . import theme
from datetime import datetime
from . import nav
from models.admindashBE import adminBE
from models import user_session


class admindashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=theme.BACKGROUND)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = nav.navbar(self, parent, mode=user_session.user_type.lower())
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

        self.searchEntry = ctk.CTkEntry( # Will only work by name
            filterFrame, 
            placeholder_text = "Search Staff..."
        )
        self.searchEntry.grid(row=0, column=0, padx=(0,5), pady=5) 

        ctk.CTkButton(
            filterFrame, 
            text="Search", 
            font=theme.BODY_FONT, 
            bg_color=theme.PRIMARY_DARK, 
            fg_color=theme.PRIMARY,
            command=self.searchStaff
        ).grid(row=0, column=1, padx=(5,0), pady=5)

        self.editStaffBtn = ctk.CTkButton( # Filter to roles
            filterFrame,
            text = "Edit",
            fg_color= theme.PRIMARY,
            hover_color= theme.PRIMARY_LIGHT,
            command = self.editStaffdrop
        )
        self.editStaffBtn.grid(row=0, column=3, padx=5, pady=5)
        
        self.addStaffBtn = ctk.CTkButton( # Connect to hidden page (like dropdowns) reveals fill-in sections with a submit button.
            filterFrame,
            text = "Add Staff",
            fg_color = theme.PRIMARY,
            hover_color = theme.PRIMARY_LIGHT,
            command = self.addStaffdrop
        )
        self.addStaffBtn.grid(row=0, column=4, padx=5)

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

        self.staffTable.bind('<<TreeviewSelect>>', self.onSelect)

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

        self.searchApt = ctk.CTkEntry( # Will only works for apt number
            filterFrame,
            placeholder_text = "Search Apartment..."
        )
        self.searchApt.grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            filterFrame, 
            text="Search", 
            font=theme.BODY_FONT, 
            bg_color=theme.PRIMARY_DARK, 
            fg_color=theme.PRIMARY,
            command=self.searchAptBox
        ).grid(row=0, column=1, padx=(5,0), pady=5)

        self.searchCity = ctk.CTkComboBox(
            filterFrame,
            values = ["All Cities", "Bristol", "Cardiff", "London", "Manchester"]
        )
        self.searchCity.grid(row=0, column=2, padx=5)

        self.searchStatus = ctk.CTkComboBox(
            filterFrame,
            values = ["All Status", "Occupied", "Available"]
        )
        self.searchStatus.grid(row=0, column=3, padx=5)

        # Same as staff details but for apartments
        tableColumns = ("Apartment", "City", "Tenant",
            "Lease Start", "Lease End", "Rent", "Status")
        self.aptTable = ttk.Treeview(card, columns=tableColumns, show="headings")

        for column in tableColumns:
            self.aptTable.heading(column, text=column)
            self.aptTable.column(column, anchor="center", width=120)
        self.aptTable.pack(fill="both", expand=True, padx=15, pady=10)

        aptData = adminBE.getAptData()

        for apt in aptData:
            aptNumber, City, Tenant, startDate, endDate, Rent, Status = apt
            Tenant = Tenant if Tenant else "-"
            startDate = startDate if startDate else "-"
            endDate = endDate if endDate else "-"
            self.aptTable.insert("", "end", values=(aptNumber, City, Tenant, 
                                               startDate, endDate, Rent, Status))
            
        self.labelFrameApt = ctk.CTkFrame(card, fg_color=theme.TITLE)
        self.labelFrameApt.pack(fill="x", padx=15, pady=10)
        self.labelFrameApt.pack_forget() 
        self.labelBannerApt = ctk.CTkLabel(self.labelFrameApt, text="", text_color=theme.SURFACE)
        self.labelBannerApt.pack(fill="x", padx=5, pady=5)

    def graphsCard(self): # Add more graphs, maybe a drop down select

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

    def refresh(self):
        for widget in self.scrollFrame.winfo_children():
            widget.destroy()

        self.manageStaffCard()
        self.manageAptCard()
        self.graphsCard()

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

    def searchStaff(self):

        term = self.searchEntry.get().strip()
        staffs = adminBE.getStaffData() ### Match my backend
        found = []

        if term:
            for staff in staffs:
                name = staff[1]
                if term in name:
                    found.append(staff)

            if found:    
                # Only clear table if successfully found result
                for w in self.staffTable.get_children():
                    self.staffTable.delete(w)

                for staff in found:
                    self.staffTable.insert("", "end", values=staff)

                # Display success banner
                self.labelFrame.pack(fill="x", padx=15, pady=10)
                self.labelBanner.configure(text="Staff Found.", fg_color=theme.SUCCESS)
                self.after(3000, lambda: self.labelFrame.pack_forget())

            else:
                # Display failed banner if unfound
                self.labelFrame.pack(fill="x", padx=15, pady=10)
                self.labelBanner.configure(text="No Staff Found.", fg_color=theme.DANGER)
                self.after(3000, lambda: self.labelFrame.pack_forget())
    
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
        roles = ["manager","admin","finance","maintenance","frontdesk"]

        if not all([fullName, Phone, Email, Password, Role]):
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Please fill all fields.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return

        if len(Phone) < 11:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Must input a valid phone number.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if "@" not in Email or "." not in Email:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Must enter a valid email", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if Role not in roles:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Must input a valid role.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if len(Password) < 8:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Password must be atleast 8 characters long.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        if not any(char.isdigit() for char in Password):
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Password must be contain a digit.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if not any(char.isalpha() for char in Password):
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Password must be contain a letter.", 
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

    def onSelect(self, event):
        selected = self.staffTable.selection()
        if not selected:
            self.selectStaffID = None
            self.selectedStaffData = None
            return

        self.selectStaffID = selected[0]
        self.selectedStaffData = self.staffTable.item(self.selectStaffID, 'values')

        if self.editStaffVisible and self.selectedStaffData:
            self.editNameEntry.delete(0, 'end')
            self.editNameEntry.insert(0, self.selectedStaffData[1])
            
            self.editPhoneEntry.delete(0, 'end')
            self.editPhoneEntry.insert(0, self.selectedStaffData[2])
            
            self.editEmailEntry.delete(0, 'end')
            self.editEmailEntry.insert(0, self.selectedStaffData[3])
            
            self.editRoleEntry.delete(0, 'end')
            self.editRoleEntry.insert(0, self.selectedStaffData[4])

    def updateStaff(self):
        if not self.selectStaffID or not self.selectedStaffData:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="No staff selected.", fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return

        userID = self.selectedStaffData[0]  # ID from Treeview
        fullName = self.editNameEntry.get().strip()
        Phone = self.editPhoneEntry.get().strip()
        Email = self.editEmailEntry.get().strip()
        Role = self.editRoleEntry.get().strip()
        roles = ["manager","admin","finance","maintenance","frontdesk"]

        if not all([fullName, Phone, Email, Role]):
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Please fill all fields.", fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if len(Phone) < 11:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Must input a valid phone number.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if "@" not in Email or "." not in Email:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Must enter a valid email", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return
        
        if Role not in roles:
            self.labelFrame.pack(fill="x", padx=15, pady=10)
            self.labelBanner.configure(text="Must input a valid role.", 
                fg_color=theme.DANGER)
            self.after(3000, lambda: self.labelFrame.pack_forget())
            return

        adminBE.editStaff(userID, fullName, Phone, Email, Role)

        self.staffTable.item(self.selectStaffID, values=(userID, fullName, Phone, Email, Role, self.selectedStaffData[5]))

        self.labelFrame.pack(fill="x", padx=15, pady=10)
        self.labelBanner.configure(text="Staff updated successfully!", fg_color=theme.SUCCESS)
        self.after(3000, lambda: self.labelFrame.pack_forget())

    def searchAptBox(self):
        term = self.searchApt.get().strip()
        cityFilter = self.searchCity.get()
        statusFilter = self.searchStatus.get()
        apts = self.aptFilters(cityFilter, statusFilter)
        found = []

        if term:
            if apts:
                for apt in apts:
                    name = apt[0]
                    if term in name:
                        found.append(apt)

                if found:    
                    # Only clear table if successfully found result
                    for w in self.aptTable.get_children():
                        self.aptTable.delete(w)

                    for apt in found:
                        self.aptTable.insert("", "end", values=apt)

                    # Display success banner
                    self.labelFrameApt.pack(fill="x", padx=15, pady=10)
                    self.labelBannerApt.configure(text="Apt Found.", fg_color=theme.SUCCESS)
                    self.after(3000, lambda: self.labelFrameApt.pack_forget())

                else:
                    # Display failed banner if unfound
                    self.labelFrameApt.pack(fill="x", padx=15, pady=10)
                    self.labelBannerApt.configure(text="No Apt Found.", fg_color=theme.DANGER)
                    self.after(3000, lambda: self.labelFrameApt.pack_forget())
            else:
                for w in self.aptTable.get_children():
                        self.aptTable.delete(w)

                self.labelFrameApt.pack(fill="x", padx=15, pady=10)
                self.labelBannerApt.configure(text="No Apt Found.", fg_color=theme.DANGER)
                self.after(3000, lambda: self.labelFrameApt.pack_forget())

    
    def aptFilters(self, cityFilter, statusFilter):
        term = self.searchApt.get().strip()

        apts = adminBE.getAptData()
        found = []

        for apt in apts:
            name = apt[0]
            aptCity = apt[1] 
            aptStatus = apt[6] 

            if term and term not in name:
                continue
            if cityFilter != "All Cities" and cityFilter != aptCity:
                continue
            if statusFilter != "All Status" and statusFilter.lower() != aptStatus.lower():
                continue

            found.append(apt)

        return found
