import os
from datetime import datetime

def generate_receipt(invoiceID, total, lateFee):
    now = datetime.now()
    receipt_text = f"""
Receipt - Invoice {invoiceID}
Date: {now.strftime('%Y-%m-%d %H:%M:%S')}

Total Paid: £{total}
Late Fee: £{lateFee}

Thank you for your payment!
"""

    # Save to receipts folder
    os.makedirs("receipts", exist_ok=True)
    filename = f"receipts/Receipt_{invoiceID}_{now.strftime('%Y%m%d%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(receipt_text)

    return filename