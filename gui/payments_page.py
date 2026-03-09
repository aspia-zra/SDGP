import tkinter as tk
from tkinter import ttk
from models.payment_model import *
from utils.receipt_generator import generate_receipt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

TENANT_ID = 1


def create_payments_page(parent):

    main = tk.Frame(parent, bg="#f5f5f5")
    main.pack(fill="both", expand=True)

    if check_late_payment(TENANT_ID):

        alert = tk.Label(
            main,
            text="Late Payment! Please pay your rent.",
            bg="red",
            fg="white",
            font=("Arial", 12, "bold")
        )

        alert.pack(fill="x")

    title = tk.Label(
        main,
        text="Payments",
        font=("Arial", 22, "bold"),
        bg="#f5f5f5"
    )

    title.pack(pady=15)

    content = tk.Frame(main, bg="#f5f5f5")
    content.pack()

    # Payment form card
    card = tk.Frame(
        content,
        bg="white",
        bd=2,
        relief="ridge",
        padx=30,
        pady=25
    )

    card.grid(row=0, column=0, padx=40)

    tk.Label(card, text="Cardholder name:", bg="white").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(card)
    name_entry.grid(row=0, column=1)

    tk.Label(card, text="Card number:", bg="white").grid(row=1, column=0, sticky="w")
    card_entry = tk.Entry(card)
    card_entry.grid(row=1, column=1)

    tk.Label(card, text="Expiry date:", bg="white").grid(row=2, column=0, sticky="w")
    expiry_entry = tk.Entry(card)
    expiry_entry.grid(row=2, column=1)

    tk.Label(card, text="CVV:", bg="white").grid(row=3, column=0, sticky="w")
    cvv_entry = tk.Entry(card)
    cvv_entry.grid(row=3, column=1)

    tk.Label(card, text="Invoice ID:", bg="white").grid(row=4, column=0, sticky="w")
    invoice_entry = tk.Entry(card)
    invoice_entry.grid(row=4, column=1)

    def pay_rent():

        invoice_id = invoice_entry.get()

        pay_invoice(invoice_id)

        generate_receipt(invoice_id, "Rent Payment")

        print("Payment successful")

    submit = tk.Button(
        card,
        text="Submit",
        bg="#1a2c8b",
        fg="white",
        width=15,
        command=pay_rent
    )

    submit.grid(row=5, columnspan=2, pady=15)

    # Pie chart
    graph_frame = tk.Frame(content, bg="#f5f5f5")
    graph_frame.grid(row=0, column=1, padx=40)

    tk.Label(graph_frame, text="Payments Graph:", font=("Arial", 12, "bold")).pack()

    data = get_payment_summary(TENANT_ID)

    labels = []
    values = []

    for row in data:
        labels.append(row[0])
        values.append(row[1])

    fig = plt.figure(figsize=(3, 3))
    plt.pie(values, labels=labels, autopct="%1.0f%%")

    canvas = FigureCanvasTkAgg(fig, graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Payment history table
    table_frame = tk.Frame(main)
    table_frame.pack(pady=20)

    table = ttk.Treeview(table_frame)

    table["columns"] = ("Amount", "DueDate", "Status")

    table.heading("#0", text="Invoice ID")
    table.heading("Amount", text="Amount")
    table.heading("DueDate", text="Due Date")
    table.heading("Status", text="Status")

    payments = get_tenant_payments(TENANT_ID)

    for p in payments:
        table.insert("", "end", text=p[0], values=(p[1], p[2], p[3]))

    table.pack()