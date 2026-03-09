from datetime import datetime

def generate_receipt(invoice_id, amount):

    filename = f"receipt_{invoice_id}.txt"

    with open(filename, "w") as file:

        file.write("PARAGON APARTMENTS\n")
        file.write("----------------------------\n")
        file.write(f"Invoice ID: {invoice_id}\n")
        file.write(f"Amount Paid: {amount}\n")
        file.write(f"Date: {datetime.now()}\n")
        file.write("Thank you for your payment.\n")

    return filename