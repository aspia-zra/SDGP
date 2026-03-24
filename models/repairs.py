""" # methods: from use case (more methods)
    book maintenance visits
    check worker availability
    chceck worker role needed
    record resolution
    log cost and time """
    
""" class: from class diagram 
attributes: self.logid=logid
logid
apartmentid
userid
maintenancedate
timetaken
cost
notes
---
operations: def (with sql statements)
logmaintenance()
calculatetotalcost()
generatemaintenancereport()

"""
from db.dbconnect import *

class Repair:
    def __init__(self, apartmentID, logID=None, userID=None, maintenanceDate=None, timeTaken=None, Cost=None, Notes=None):
         self.logID = logID
         self.apartmentID = apartmentID
         self.userID = userID
         self.maintenanceDate = maintenanceDate 
         self.timeTaken = timeTaken
         self.Cost= Cost
         self.Notes= Notes
         #db = cursor()
    
    @staticmethod  # it's the same as booking the maintenance too   
    def log_maintenance(db, apartmentID, userID, maintenanceDate):
        query = """
        INSERT INTO MaintenanceLog
        (apartmentID, userID, maintenanceDate, Notes)
        VALUES (%s, %s, %s, %s)
        """
        db.execute(query, (apartmentID, userID, maintenanceDate, None))
    
    @staticmethod
    def calculate_total_cost(db, apartment_id):
        query = """
            SELECT SUM(Cost)
            FROM MaintenanceLog
            WHERE apartmentID=%s
        """
        result = db.fetch_one(query, (apartment_id,))
        return result[0] if result[0] else 0

    @staticmethod 
    def generate_report(db): # ask imaan though
        query = "SELECT * FROM MaintenanceLog"
        return db.fetch_all(query)
     
    @staticmethod # same as log cost and time, removed for redundancy
    def record_resolution(db, log_id, time_taken, cost, notes):
        query = """
            UPDATE MaintenanceLog
            SET timeTaken=%s, Cost=%s, Notes=%s
            WHERE logID=%s
        """
        db.execute(query, (time_taken, cost, notes, log_id))

    @staticmethod
    def check_availability(db, user_id, date):
        query = """
            SELECT COUNT(*)
            FROM MaintenanceLog
            WHERE userID = %s AND DATE(maintenanceDate) = DATE(%s)
        """
        result = db.fetch_one(query, (user_id, date))
        return result[0] == 0  # True if available
            
    @staticmethod
    def check_role(db, user_id, required_role="maintenance"):
        query = "SELECT Role FROM UserTbl WHERE userID = %s"
        role = db.fetch_one(query, (user_id,))

        if role is None:
            return False

        return role[0] == required_role
    # 22/02 as we dont have dummy data in the user table, it used to crash if the worker didnt exist
