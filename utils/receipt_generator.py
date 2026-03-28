from datetime import datetime


def generate_receipt(invoiceID, total, lateFee):

    filename = f"receipt_{invoiceID}.txt"

    # ✅ calculate base rent properly
    base_rent = float(total) - float(lateFee)

    # ✅ clean date format
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M")

    with open(filename, "w") as f:

        f.write("=====================================\n")
        f.write("        RENT PAYMENT RECEIPT\n")
        f.write("=====================================\n\n")

        f.write(f"Invoice ID : {invoiceID}\n")
        f.write(f"Date       : {date_now}\n\n")

        f.write("-------------------------------------\n")
        f.write(f"Base Rent  : £{base_rent:.2f}\n")
        f.write(f"Late Fee   : £{float(lateFee):.2f}\n")
        f.write("-------------------------------------\n")
        f.write(f"Total Paid : £{float(total):.2f}\n")
        f.write("-------------------------------------\n\n")

        f.write("Status     : PAID\n\n")
        f.write("Thank you for your payment.\n")
        f.write("=====================================\n")

    return filename