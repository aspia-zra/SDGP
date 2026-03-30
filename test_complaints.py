# Key functions:
# Get tenant info using apartment number
# - test success, accurate info entered
# - failure for non existing apt number
# - failure for existing apt number but no lease.

# Add a complaint to the db using provided info
# - tests success, accurate info entered
# - failure, invalid apt number
# - failure, no active tenant in apt (leaseAgreement)
# - missing reason - should still implement as its no necessary for submit  

import unittest, os, sys
from models.complaints import Complaints
from db.db_connect import Database

class TestComplaints(unittest.TestCase):
    # Testing tenant search func: 
    def test_validTenantSearch(self):
        db = Database()
        complaints_instance = Complaints(db)
        tenant_id = complaints_instance.get_tenantID("A102")
        self.assertEqual(tenant_id, 2)
        if hasattr(db, 'close'): 
            db.close() 

    def test_invalidApt(self):
        db = Database()
        complaints_instance = Complaints(db)
        tenant_id = complaints_instance.get_tenantID("NILNIL")
        self.assertIsNone(tenant_id)
        if hasattr(db, 'close'): 
            db.close() 

    def test_invalidLease(self):
        db = Database()
        complaints_instance = Complaints(db)
        tenant_id = complaints_instance.get_tenantID("NILNIL")
        self.assertIsNone(tenant_id)
        if hasattr(db, 'close'): 
            db.close() 
    
    # Testing add complaint func: 
    def test_validAddComplaint(self):
        db = Database()
        complaints_instance = Complaints(db)
        result = complaints_instance.add_complaint("Heating not working", "3", "A102", "Broken heater")
        self.assertTrue(result)
        if hasattr(db, 'close'): 
            db.close() 

    def test_invalidAptAdd(self):
        db = Database()
        complaints_instance = Complaints(db)
        result = complaints_instance.add_complaint("Invalid apt test", "2", "NILNIL", "Invalid apt test")
        self.assertFalse(result)
        if hasattr(db, 'close'): 
            db.close() 

    def test_invalidTenant(self):
        db = Database()
        complaints_instance = Complaints(db)
        result = complaints_instance.add_complaint("Empty apt test", "1", "NILNIL", "Invalid Lease")
        self.assertFalse(result)
        if hasattr(db, 'close'): 
            db.close() 

    def test_missingReason(self):
        db = Database()
        complaints_instance = Complaints(db)
        result = complaints_instance.add_complaint("", "2", "A102", "Missing reason test")
        self.assertTrue(result)
        if hasattr(db, 'close'): 
            db.close() 

if __name__ == '__main__':
    unittest.main()
