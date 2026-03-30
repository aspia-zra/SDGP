from datetime import datetime
 
 
def generate_receipt(invoice_id, tenant_name, amount, due_date, status):
    filename = f"receipt_{invoice_id}.txt"
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
    with open(filename, "w") as f:
        f.write(content)
    return filename, content
 