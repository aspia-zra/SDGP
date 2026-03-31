import customtkinter as ctk
import os
from tkinter import messagebox
from models import user_session
from gui.payment_page import PaymentPage

# pretest
# prevent script from stopping for manual input.
messagebox.showinfo = lambda title, msg: print(f"  [LOG] Info Popup: {title} - {msg}")
messagebox.showwarning = lambda title, msg: print(f"  [LOG] Warning Popup: {title} - {msg}")

def run_big_bang_transaction():
    print("Initializing Big-Bang Integration Test...")
    
    #setup global state
    user_session.user_type = "Finance"
    
    root = ctk.CTk()
    #load actual frame with all real imports and dependencies
    app = PaymentPage(root)
    app.pack(expand=True, fill="both")
    
    #process initial load_invoices() calls within constructor
    root.update()

    try:
        #step 1: UI-to-Model Data Fetch
        #verifies if treeview correctly populates from database model
        rows = app.table.get_children()
        if not rows:
            print("INTEGRATION ERROR: PaymentPage failed to pull data from payment_model.")
            return

        #select first invoice record for testing
        target = rows[0]
        initial_values = app.table.item(target)["values"]
        invoice_id = initial_values[0]
        
        print(f"Found Invoice {invoice_id}. Current Status: {initial_values[4]}")
        app.table.selection_set(target)

        #step 2:logic-to-database update
        print("Simulating 'Mark as Paid' click...")
        app.mark_as_paid() 
        root.update() #this triggers the reload

        new_rows = app.table.get_children()
        
        updated_row = None
        for row_id in new_rows:
            if app.table.item(row_id)["values"][0] == invoice_id:
                updated_row = row_id
                break
        
        if updated_row:
            updated_status = app.table.item(updated_row)["values"][4]
            if updated_status.lower() == "paid":
                print("SUCCESS: UI -> Model -> Database integration verified.")
            else:
                print(f"FAIL: Database state did not sync with UI (Status: {updated_status}).")
        else:
            print(f"FAIL: Invoice {invoice_id} disappeared from the table after refresh.")
        # step 3: Receipt Generation
        print("Simulating 'Generate Receipt'...")
        app.generate_receipt()
        root.update()

        popups = [child for child in root.winfo_children() if isinstance(child, ctk.CTkToplevel)]
        if popups:
            print("SUCCESS: Receipt Preview UI integrated.")
            popups[0].destroy()
        
        receipt_found = any(str(invoice_id) in f for f in os.listdir('.') if f.endswith(('.txt', '.pdf')))
        if receipt_found:
            print("SUCCESS: File System Integration (Receipt generated on disk).")
        else:
            print("FAIL: Receipt utility did not create a physical file.")

    except Exception as e:
        print(f"SYSTEM CRASH during Big-Bang: {e}")
    
    finally:
        print("Big-Bang Test Cycle Finished.")
        root.destroy()

if __name__ == "__main__":
    run_big_bang_transaction()
