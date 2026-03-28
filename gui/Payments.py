from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

from . import NavBar
from models.paymentBE import *
import models.user_session as user_session
from utils.receipt_generator import generate_receipt


class payments(ctk.CTkFrame):

    def __init__(self, main):

        super().__init__(main)

        self.grid(row=0, column=0, sticky="nsew")

        self.nav = NavBar.navbar(self, main)
        self.nav.grid(row=0, column=0, sticky="ns")

        self.create_layout()

    def create_layout(self):

        mainFrame = Frame(self)
        mainFrame.grid(row=0, column=1, padx=20, pady=20)

        Label(mainFrame, text="Payments", font=("Arial", 24)).pack()

        # ⚠ Overdue warning
        if check_late_payment():
            Label(
                mainFrame,
                text="⚠ Overdue Rent Detected",
                fg="#9C2007",
                font=("Arial", 14, "bold")
            ).pack(pady=10)

        columns = ("InvoiceID", "Amount", "DueDate", "Status")

        self.table = ttk.Treeview(
            mainFrame,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            self.table.heading(col, text=col)

        self.table.pack(pady=10)

        # Row colours
        self.table.tag_configure("paid", foreground="green")
        self.table.tag_configure("overdue", foreground="red")
        self.table.tag_configure("pending", foreground="orange")

        self.load_payments()

        self.table.bind("<<TreeviewSelect>>", self.select_invoice)

        ctk.CTkButton(
            mainFrame,
            text="Pay Selected Invoice",
            fg_color="#202e75",
            hover_color="#0f0f30",
            command=self.process_payment
        ).pack(pady=10)

        self.create_graph(mainFrame)

    def load_payments(self):
        payments = get_payments()

        for row in payments:

            invoiceID = row['invoiceID']
            amount = float(row['Amount'])
            dueDate = row['dueDate']
            status = row['Status'].lower()

         # ✅ calculate late fee
            if status == "overdue":
                late_fee = calculate_late_fee(amount)
            else:
                late_fee = 0

            total = amount + late_fee

            # tags for colouring
            if status == "paid":
                tag = "paid"
            elif status == "overdue":
                tag = "overdue"
            else:
                tag = "pending"

            status_display = f"{status} | Late: £{late_fee} | Total: £{total}"

            self.table.insert(
                "",
                END,
                values=(invoiceID, f"£{amount}", dueDate, status_display),
                tags=(tag,)
            )

    def select_invoice(self, event):

        selected = self.table.focus()

        values = self.table.item(selected, "values")

        if values:
            self.invoiceID = int(values[0])  # ✅ ensure it's an int

    def process_payment(self):

        if not hasattr(self, "invoiceID"):
            messagebox.showerror("Error", "Select invoice first")
            return

    # ✅ get total + late fee from backend
        total, lateFee = pay_invoice(self.invoiceID)

    # ✅ generate receipt (includes late fee)
        receipt = generate_receipt(self.invoiceID, total, lateFee)

    # ✅ show BOTH total and late fee to user
        messagebox.showinfo(
            "Success",
            f"Payment complete\n\nTotal Paid: £{total}\nLate Fee: £{lateFee}\n\nReceipt saved: {receipt}"
        )

        # 🔄 refresh table after payment
        for row in self.table.get_children():
            self.table.delete(row)

        self.load_payments()

    def create_graph(self, frame):

        data = get_payment_summary()

        labels = [x[0] for x in data]
        values = [x[1] for x in data]

        fig, ax = plt.subplots(figsize=(4, 3))

        ax.pie(values, labels=labels, autopct="%1.1f%%")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()