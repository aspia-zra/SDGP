#from datetime import datetime

#def generate_receipt(invoice_id, tenant_name, amount, due_date, status):
    #filename = f"receipt_{invoice_id}.txt"
    #content = f"""{'='*40}
   #PARAGON APARTMENT MANAGEMENT
         #PAYMENT RECEIPT
#{'='*40}
#Receipt Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}
#Invoice ID   : {invoice_id}
#Tenant Name  : {tenant_name}
#Amount       : {amount}
#Due Date     : {due_date}
#Status       : {status}
#{'='*40}
#Thank you for your payment.
#"""
   # with open(filename, "w") as f:
       # f.write(content)
   # return filename, content

import os
from datetime import datetime


def generate_receipt(invoice_id, tenant_name, amount, due_date, status):

    base_dir = os.path.dirname(__file__) 
    receipts_dir = os.path.join(base_dir, "receipts")

    os.makedirs(receipts_dir, exist_ok=True)

    filename = f"receipt_{invoice_id}.txt"
    file_path = os.path.join(receipts_dir, filename)

    content = f"""{'='*40}
   PARAGON APARTMENT MANAGEMENT
         PAYMENT RECEIPT
{'='*40}
Receipt Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}
Invoice ID   : {invoice_id}
Tenant Name  : {tenant_name}
Amount       : {amount}
Due Date     : {due_date}
Status       : {status}
{'='*40}
Thank you for your payment.
"""

    with open(file_path, "w") as f:
        f.write(content)

    return file_path, content
