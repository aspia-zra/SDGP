import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from gui import theme
from gui import navbar
from models import user_session


class PaymentPage(ctk.CTkFrame):

    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color=theme.BACKGROUND)
        self.controller = controller

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = navbar.navbar(self, parent, mode=user_session.user_type.lower())
        self.nav.grid(row=0, rowspan=2, column=0, sticky="ns")

        # header
        hdr = ctk.CTkFrame(self, fg_color=theme.SURFACE, height=70, corner_radius=0)
        hdr.grid(row=0, column=1, sticky="ew")
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="Payment & Billing",
                     font=theme.TITLE_FONT,
                     text_color=theme.PRIMARY).grid(row=0, column=0, sticky="w", padx=30, pady=10)
        ctk.CTkLabel(hdr, text="Finance Manager — Manage all tenant invoices",
                     font=theme.BODY_FONT,
                     text_color=theme.TEXT_SECONDARY).grid(row=1, column=0, sticky="w", padx=30, pady=(0, 10))

        # main content
        self.content = ctk.CTkFrame(self, fg_color=theme.BACKGROUND, corner_radius=0)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        # alert banner
        self.alert_label = ctk.CTkLabel(
            self.content,
            text="⚠️ There are overdue invoices! Please review.",
            fg_color=theme.DANGER,
            text_color="white",
            font=("Helvetica", 12, "bold"),
            corner_radius=0,
            height=35
        )

        # buttons
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=15)

        ctk.CTkButton(btn_frame, text="Mark as Paid", width=150, height=38, corner_radius=8,
                      font=("Helvetica", 12, "bold"), fg_color=theme.PRIMARY,
                      hover_color=theme.PRIMARY_DARK, command=self.mark_as_paid).grid(row=0, column=0, padx=8)

        ctk.CTkButton(btn_frame, text="Generate Receipt", width=150, height=38, corner_radius=8,
                      font=("Helvetica", 12, "bold"), fg_color=theme.SUCCESS,
                      hover_color="#0e9063", command=self.generate_receipt).grid(row=0, column=1, padx=8)

        ctk.CTkButton(btn_frame, text="Show Overdue", width=150, height=38, corner_radius=8,
                      font=("Helvetica", 12, "bold"), fg_color=theme.DANGER,
                      hover_color="#922b21", command=self.show_overdue).grid(row=0, column=2, padx=8)

        ctk.CTkButton(btn_frame, text="Refresh", width=100, height=38, corner_radius=8,
                      font=("Helvetica", 12), fg_color=theme.PRIMARY,
                      hover_color=theme.PRIMARY_DARK, command=self.load_invoices).grid(row=0, column=3, padx=8)

        ctk.CTkButton(btn_frame, text="Reset", width=100, height=38, corner_radius=8,
                      font=("Helvetica", 12), fg_color=theme.WARNING,
                      hover_color="#d97706", command=self.reset_invoice).grid(row=0, column=4, padx=8)

        # table
        table_frame = ctk.CTkFrame(self.content, fg_color=theme.SURFACE, corner_radius=14)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 10))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Payment.Treeview", background=theme.BACKGROUND,
                        foreground=theme.TEXT_PRIMARY, rowheight=30,
                        fieldbackground=theme.BACKGROUND, font=("Helvetica", 11))
        style.configure("Payment.Treeview.Heading", background=theme.PRIMARY,
                        foreground="white", font=("Helvetica", 11, "bold"), relief="flat")
        style.map("Payment.Treeview", background=[("selected", theme.PRIMARY_LIGHT)])

        self.table = ttk.Treeview(table_frame,
                                   columns=("InvoiceID", "Tenant", "Amount", "DueDate", "Status"),
                                   show="headings", style="Payment.Treeview", height=15)

        self.table.heading("InvoiceID", text="Invoice ID")
        self.table.heading("Tenant", text="Tenant Name")
        self.table.heading("Amount", text="Amount (£)")
        self.table.heading("DueDate", text="Due Date")
        self.table.heading("Status", text="Status")

        self.table.column("InvoiceID", width=90, anchor="center")
        self.table.column("Tenant", width=180)
        self.table.column("Amount", width=110, anchor="center")
        self.table.column("DueDate", width=120, anchor="center")
        self.table.column("Status", width=110, anchor="center")

        self.table.tag_configure("overdue", foreground=theme.DANGER)
        self.table.tag_configure("paid", foreground=theme.SUCCESS)
        self.table.tag_configure("pending", foreground=theme.WARNING)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

        self.status_label = ctk.CTkLabel(self.content, text="",
                                          font=theme.SMALL_FONT, text_color=theme.TEXT_SECONDARY)
        self.status_label.grid(row=3, column=0, pady=(0, 10))

        self.load_invoices()

    def load_invoices(self):
        for row in self.table.get_children():
            self.table.delete(row)
        try:
            from models.payment_model import get_all_invoices, check_any_overdue
            invoices = get_all_invoices()
            for invoice in invoices:
                invoice_id = invoice[0]
                tenant_name = invoice[1]
                amount = f"£{invoice[2]:.2f}"
                due_date = str(invoice[3])
                status = invoice[4]
                tag = status.lower()
                self.table.insert("", "end", values=(invoice_id, tenant_name, amount, due_date, status), tags=(tag,))
            if check_any_overdue():
                self.alert_label.grid(row=0, column=0, sticky="ew")
            else:
                self.alert_label.grid_remove()
            self.status_label.configure(text=f"{len(invoices)} invoices loaded")
        except Exception as e:
            self.status_label.configure(text="Could not load invoices — check database connection")
            print("Error loading invoices:", e)

    def mark_as_paid(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an invoice first")
            return
        invoice_id = self.table.item(selected[0])["values"][0]
        status = self.table.item(selected[0])["values"][4]
        if status == "paid":
            messagebox.showinfo("Info", "This invoice is already paid")
            return
        try:
            from models.payment_model import mark_invoice_paid
            mark_invoice_paid(invoice_id)
            messagebox.showinfo("Success", f"Invoice {invoice_id} marked as paid")
            self.load_invoices()
        except Exception as e:
            messagebox.showerror("Error", "Could not update invoice")
            print("Error marking paid:", e)

    def generate_receipt(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an invoice first")
            return
        values = self.table.item(selected[0])["values"]
        try:
            from utils.receipt_generator import generate_receipt
            filename, content = generate_receipt(values[0], values[1], values[2], values[3], values[4])

            # show preview popup
            popup = ctk.CTkToplevel(self)
            popup.title("Receipt Preview")
            popup.geometry("420x380")
            popup.grab_set()

            ctk.CTkLabel(popup, text="Receipt Preview",
                         font=("Helvetica", 16, "bold"),
                         text_color=theme.PRIMARY).pack(pady=(20, 10))

            text_box = ctk.CTkTextbox(popup, width=360, height=220, font=("Courier", 12))
            text_box.pack(padx=20)
            text_box.insert("1.0", content)
            text_box.configure(state="disabled")

            ctk.CTkLabel(popup, text=f"Saved as {filename}",
                         font=("Helvetica", 11),
                         text_color="gray").pack(pady=(8, 0))

            ctk.CTkButton(popup, text="Close",
                          fg_color=theme.PRIMARY,
                          hover_color=theme.PRIMARY_DARK,
                          command=popup.destroy).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Error", "Could not generate receipt")
            print("Error generating receipt:", e)

    def reset_invoice(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an invoice first")
            return
        invoice_id = self.table.item(selected[0])["values"][0]
        try:
            from models.payment_model import reset_invoice_status
            reset_invoice_status(invoice_id)
            messagebox.showinfo("Reset", f"Invoice {invoice_id} reset to pending")
            self.load_invoices()
        except Exception as e:
            messagebox.showerror("Error", "Could not reset invoice")
            print("Error resetting invoice:", e)

    def show_overdue(self):
        for row in self.table.get_children():
            self.table.delete(row)
        try:
            from models.payment_model import get_overdue_invoices
            invoices = get_overdue_invoices()
            for invoice in invoices:
                invoice_id = invoice[0]
                tenant_name = invoice[1]
                amount = f"£{invoice[2]:.2f}"
                due_date = str(invoice[3])
                status = invoice[4]
                self.table.insert("", "end", values=(invoice_id, tenant_name, amount, due_date, status), tags=("overdue",))
            self.status_label.configure(text=f"{len(invoices)} overdue invoices")
        except Exception as e:
            self.status_label.configure(text="Could not load overdue invoices")
            print("Error:", e)