from tkinter import *
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter.ttk import Progressbar
from . import NavBar
from Models.admindashBE import progressbarCalc, dropdownBoxes, graph

class admindashboard(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)
        self.main = main

        self.grid(row=0, column=0, sticky="nsew") 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.nav = NavBar.navbar(self, self.main)
        self.nav.grid(row=0, column=0, sticky="ns")

        self.admindash()

    def admindash(self):
        self.dashboardFrame = Frame(self)
        self.dashboardFrame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.dashboardFrame.grid_columnconfigure(0, weight=2)
        self.dashboardFrame.grid_columnconfigure(1, weight=1)
        self.dashboardFrame.grid_rowconfigure(0, weight=1)

    # Progress Bars
        progressFrame = Frame(self.dashboardFrame)
        progressFrame.grid(row = 0, column = 0, pady = 20)
        aptPercent, invoicePercent, compPercent = progressbarCalc()

        apartments = Label(progressFrame, text="Apartments Occupied")
        apartments.grid(row = 0, column = 0,pady = 20)

        aptProgress = Progressbar(progressFrame, orient=HORIZONTAL, length=200, mode='determinate')
        aptProgress['value'] = aptPercent
        aptProgress.grid(row = 1, column = 0,pady = 20)

        rentCollected = Label(progressFrame, text="Rent Collected")
        rentCollected.grid(row = 2, column = 0,pady = 20)

        rentProgress = Progressbar(progressFrame, orient=HORIZONTAL, length=200, mode='determinate')
        rentProgress['value'] = invoicePercent
        rentProgress.grid(row = 3, column = 0,pady = 20)

        repairsMade = Label(progressFrame, text="Complaints Resolved")
        repairsMade.grid(row = 4, column = 0,pady = 20)

        repairsProgress = Progressbar(progressFrame, orient=HORIZONTAL, length=200, mode='determinate')
        repairsProgress['value'] = compPercent
        repairsProgress.grid(row = 5, column = 0,pady = 20)

    # Quick actions
        quickActionsFrame = Frame(self.dashboardFrame)
        quickActionsFrame.grid(row= 1, column=0, padx=20, pady=20)
        
        quickActions = Label(quickActionsFrame, text="Quick Actions", font=("Arial", 18))
        quickActions.grid(row=0, column=0, columnspan=3, pady=20)

        addAptButton = Button(quickActionsFrame, text="Add Apartment", width=10)
        addAptButton.grid(row=1, column=0, padx=10)

        createLeaseButton = Button(quickActionsFrame, text="Create Lease", width=10)
        createLeaseButton.grid(row=1, column=1, padx=10)

        generalReportButton = Button(quickActionsFrame, text="General Report", width=10)
        generalReportButton.grid(row=1, column=2, padx=10)

    # Dropdowns
        dropdownsFrame = Frame(self.dashboardFrame)
        dropdownsFrame.grid(row=0, column=1, padx=20, pady=20)
        leases, overdues, repairs = dropdownBoxes()

        # Expiring Leases
        leasesFrame = Frame(dropdownsFrame)
        leasesFrame.grid(row=0, column=0, pady = 20)

        self.leaseExpiring = False
        self.leasesBtn = ctk.CTkButton(
            leasesFrame,
            text="Leases Expiring ▼",
            font=("Arial", 14),
            fg_color= '#9C2007',
            command=self.leasesDrop
        )
        self.leasesBtn.grid(row=0, column=0, padx=10, sticky="ew")

        self.leaseDetails = ctk.CTkFrame(leasesFrame)
        self.leaseDetails.grid(row=1, column=0, sticky="ew")
        self.leaseDetails.grid_remove()        

        if leases:
            for lease in leases:
                endDate = lease[0]
                fullName = lease[1]

                label = ctk.CTkLabel(
                    self.leaseDetails,
                    text=f"{fullName} | Lease Expiry: {endDate}"
                )
                label.pack(anchor="w", padx=10)
        else:
            label = ctk.CTkLabel(
                self.leaseDetails,
                text="No Expiring Leases."
            )
            label.pack(anchor="w", padx=10) 

        # Overdue Invoices
        OverdueFrame = Frame(dropdownsFrame)
        OverdueFrame.grid(row=1, column=0, pady=10)

        self.overdueRent = False
        self.overdueBtn = ctk.CTkButton(
            OverdueFrame,
            text="Overdue Rent ▼",
            font=("Arial", 14),
            fg_color= '#9C2007',
            command=self.overdueDrop
        )
        self.overdueBtn.grid(row=0, column=0, padx=10, sticky="ew")

        self.overdueDetails = ctk.CTkFrame(OverdueFrame)
        self.overdueDetails.grid(row=1, column=0, sticky="ew")
        self.overdueDetails.grid_remove()        

        if overdues:
            for item in overdues:
                amount = item[0]
                dueDate = item[1]
                fullName = item[2]

                label = ctk.CTkLabel(
                    self.overdueDetails,
                    text=f"{fullName} | £{amount} Due: {dueDate}"
                )
                label.pack(anchor="w", padx=10)
        else:
            label = ctk.CTkLabel(
                self.overdueDetails,
                text="No Overdue Payments."
            )
            label.pack(anchor="w", padx=10)
        
        # High Priority Repairs
        highPriorityFrame = Frame(dropdownsFrame)
        highPriorityFrame.grid(row=2, column=0, pady=10)

        self.highRepairs = False
        self.highRepairBtn = ctk.CTkButton(
            highPriorityFrame,
            text="High Priority Repairs ▼",
            font=("Arial", 14),
            fg_color= '#9C2007',
            command=self.repairsDrop
        )
        self.highRepairBtn.grid(row=0, column=0, padx=10, sticky="ew")

        self.repairDetails = ctk.CTkFrame(highPriorityFrame)
        self.repairDetails.grid(row=1, column=0, sticky="ew")
        self.repairDetails.grid_remove()        

        if repairs:
            for repair in repairs:
                severity = repair[0]
                cost = repair[1]
                fullName = repair[2]

                label = ctk.CTkLabel(
                    self.repairDetails,
                    text=f"{fullName} | £{cost} Severity: {severity}"
                )
                label.pack(anchor="w", padx=10)
        else:
            label = ctk.CTkLabel(
                self.repairDetails,
                text="No Repairs."
            )
            label.pack(anchor="w", padx=10)

    # Graphs
        graphFrame = Frame(self.dashboardFrame)
        graphFrame.grid(row=1, column=1, padx=20, pady=20)

        graphsFrame = Frame(graphFrame)
        graphsFrame.grid(row=1, column=0, pady=10)

        graphs = Label(graphsFrame, text="Graphs", font=("Arial", 18))
        graphs.grid(row=0, column=0, pady=20)

        items = graph()
        months =[]
        profits =[]

        for month, profit in items:
            months.append(month)
            profits.append(profit)

        fig, ax = plt.subplots(figsize=(5,2))
        ax.plot(months, profits)
        ax.set_title("Profit Trajectory")
        ax.set_xlabel("Year-Month")
        ax.set_ylabel("Profit")

        canvas = FigureCanvasTkAgg(fig, master=graphsFrame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        

    def leasesDrop(self):
        if self.leaseExpiring:
            self.leasesBtn.configure(text="Leases Expiring ▲")
            self.leaseDetails.grid_remove()
            self.leaseExpiring = False
        else:
            self.leasesBtn.configure(text="Leases Expiring ▼")
            self.leaseDetails.grid()
            self.leaseExpiring = True

    def overdueDrop(self):
        if self.overdueRent:
            self.overdueBtn.configure(text="Overdue Rent ▲")
            self.overdueDetails.grid_remove()
            self.overdueRent = False
        else:
            self.overdueBtn.configure(text="Overdue Rent ▼")
            self.overdueDetails.grid()
            self.overdueRent = True
    
    def repairsDrop(self):
        if self.highRepairs:
            self.highRepairBtn.configure(text="High Priority Repairs ▲")
            self.repairDetails.grid_remove()
            self.highRepairs = False
        else:
            self.highRepairBtn.configure(text="High Priority Repairs ▼")
            self.repairDetails.grid()
            self.highRepairs = True
