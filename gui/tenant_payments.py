import customtkinter as ctk
from tkinter import Frame, Label, ttk, messagebox
from models.paymentBE import *
import models.user_session as user_session
from utils.receipt_generator import generate_receipt

def validate_card(number, expiry, cvv):
   
    number = number.replace(" ", "")

   
    if not number.isdigit() or len(number) not in [13, 16]:
        return False, "Invalid card number"

    if not cvv.isdigit() or len(cvv) != 3:
        return False, "Invalid CVV"

    try:
        month, year = expiry.split("/")
        month = int(month)
        year = int(year)

        if month < 1 or month > 12:
            return False, "Invalid expiry month"
    except:
        return False, "Invalid expiry format (MM/YY)"

  
    def luhn_check(card_number):
        total = 0
        reverse_digits = card_number[::-1]

        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        return total % 10 == 0

    if not luhn_check(number):
        return False, "Card number failed validation"

    return True, "Valid"

class TenantPayments(ctk.CTkFrame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
     
        from .nav import navbar  
        self.nav = navbar(self, controller)
        self.nav.tenant_nav()
        self.nav.grid(row=0, column=0, sticky="ns")

        self.create_layout()

    def create_layout(self):
        update_overdue_invoices()

        mainFrame = Frame(self)
        mainFrame.grid(row=0, column=1, padx=20, pady=20)

        Label(mainFrame, text="Payments", font=("Arial", 24)).pack()

        if check_late_payment():
            Label(mainFrame, text="⚠ Overdue Rent Detected", fg="#9C2007",
                  font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("InvoiceID", "Amount", "DueDate", "Status")
        self.table = ttk.Treeview(mainFrame, columns=columns, show="headings", height=8)
        for col in columns:
            self.table.heading(col, text=col)
        self.table.pack(pady=10)

        self.table.tag_configure("paid", foreground="green")
        self.table.tag_configure("overdue", foreground="red")
        self.table.tag_configure("pending", foreground="orange")

        self.load_payments()
        self.table.bind("<<TreeviewSelect>>", self.select_invoice)

        ctk.CTkButton(mainFrame, text="Pay Selected Invoice", fg_color="#202e75",
                      hover_color="#0f0f30", command=self.process_payment).pack(pady=10)

        self.create_graph(mainFrame)

    def load_payments(self):
        payments = get_payments()
        for row in payments:
            invoiceID = row['invoiceID']
            amount = float(row['Amount'])
            dueDate = row['dueDate']
            status = row['Status'].lower()

            late_fee = calculate_late_fee(amount) if status == "overdue" else 0
            total = amount + late_fee

            if status == "paid":
                tag = "paid"
            elif status == "overdue":
                tag = "overdue"
            else:
                tag = "pending"

            status_display = f"{status} | Late: £{late_fee} | Total: £{total}"

            self.table.insert("", "end", values=(invoiceID, f"£{amount}", dueDate, status_display), tags=(tag,))

    def select_invoice(self, event):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        if values:
            self.invoiceID = int(values[0])

    def process_payment(self):
        if not hasattr(self, "invoiceID"):
            messagebox.showerror("Error", "Select invoice first")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Enter Card Details")
        popup.geometry("300x300")

        ctk.CTkLabel(popup, text="Card Number").pack(pady=5)
        card_entry = ctk.CTkEntry(popup)
        card_entry.pack()

        ctk.CTkLabel(popup, text="Expiry (MM/YY)").pack(pady=5)
        expiry_entry = ctk.CTkEntry(popup)
        expiry_entry.pack()

        ctk.CTkLabel(popup, text="CVV").pack(pady=5)
        cvv_entry = ctk.CTkEntry(popup, show="*")
        cvv_entry.pack()

        def confirm_payment():
            card = card_entry.get()
            expiry = expiry_entry.get()
            cvv = cvv_entry.get()

            valid, msg = validate_card(card, expiry, cvv)

            if not valid:
                messagebox.showerror("Card Error", msg)
                return

            total, lateFee = pay_invoice(self.invoiceID)
            receipt = generate_receipt(self.invoiceID, total, lateFee)

            messagebox.showinfo(
                "Success",
                f"Payment complete\n\nTotal Paid: £{total}\nLate Fee: £{lateFee}\n\nReceipt saved: {receipt}"
            )

            popup.destroy()

            for row in self.table.get_children():
                self.table.delete(row)
            self.load_payments()

        ctk.CTkButton(popup, text="Confirm Payment", command=confirm_payment).pack(pady=20)

    def create_graph(self, frame):
        data = get_payment_summary()
        labels = [x[0] for x in data]
        values = [x[1] for x in data]

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(values, labels=labels, autopct="%1.1f%%")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()