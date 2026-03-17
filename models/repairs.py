# using 'maintenance log' from class diagram
# some functions in here actually make sense to go in the complaints class
# class diagram actually has to change to reflect the implemented functions

class Repair:

    def __init__(self, apartmentID, logID=None, userID=None, maintenanceDate=None, timeTaken=None, Cost=None, Notes=None):
        self.logID = logID
        self.apartmentID = apartmentID
        self.userID = userID
        self.maintenanceDate = maintenanceDate
        self.timeTaken = timeTaken
        self.Cost = Cost
        self.Notes = Notes


    @staticmethod
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
        return result[0] if result and result[0] else 0


    @staticmethod
    def generate_report(db):
        query = "SELECT * FROM MaintenanceLog"
        return db.fetch_all(query)


    @staticmethod
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
        return result[0] == 0


    @staticmethod
    def check_role(db, user_id, required_role="maintenance"):
        query = "SELECT Role FROM UserTbl WHERE userID = %s"
        role = db.fetch_one(query, (user_id,))

        if role is None:
            return False

        return role[0] == required_role



# Complaint helper functions


    @staticmethod
    def get_open_complaints(db):
        query = """
        SELECT complaintID, apartmentID, Description, reportDate, Severity
        FROM Complaint
        WHERE Status = 'open'
        """
        return db.fetch_all(query)


    @staticmethod
    def get_closed_complaints(db):
        query = """
        SELECT complaintID, apartmentID, Description, reportDate, Resolution
        FROM Complaint
        WHERE Status = 'closed'
        """
        return db.fetch_all(query)


# -----------------------------
# Repair helper functions
# -----------------------------

    @staticmethod
    def get_open_repairs(db):
        query = """
        SELECT logID, apartmentID, userID, maintenanceDate, Notes
        FROM MaintenanceLog
        WHERE timeTaken IS NULL
        """
        return db.fetch_all(query)


    @staticmethod
    def get_completed_repairs(db):
        query = """
        SELECT logID, apartmentID, userID, maintenanceDate, timeTaken, Cost, Notes
        FROM MaintenanceLog
        WHERE timeTaken IS NOT NULL
        """
        return db.fetch_all(query)


    @staticmethod
    def close_complaint(db, complaint_id, resolution):
        query = """
        UPDATE Complaint
        SET Status = 'closed',
            Resolution = %s
        WHERE complaintID = %s
        """
        db.execute(query, (resolution, complaint_id))


    @staticmethod
    def complete_repair(db, log_id, time_taken, cost, notes):
        query = """
        UPDATE MaintenanceLog
        SET timeTaken = %s,
            Cost = %s,
            Notes = %s
        WHERE logID = %s
        """
        db.execute(query, (time_taken, cost, notes, log_id))


# -----------------------------
# Dashboard request functions
# -----------------------------

    @staticmethod
    def get_openrequests(db):

        complaints = Repair.get_open_complaints(db)
        repairs = Repair.get_open_repairs(db)

        requests = []

        for c in complaints:
            requests.append({
                "id": c["complaintID"],
                "type": "complaint",
                "apartment": c["apartmentID"],
                "issue": c["Description"],
                "date": c["reportDate"],
                "worker": None,
                "priority": c["Severity"]
            })

        for r in repairs:
            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": r["Notes"],
                "date": r["maintenanceDate"],
                "worker": r["userID"],
                "priority": None
            })

        return requests


    @staticmethod
    def get_completed_requests(db):

        complaints = Repair.get_closed_complaints(db)
        repairs = Repair.get_completed_repairs(db)

        requests = []

        for c in complaints:
            requests.append({
                "id": c["complaintID"],
                "type": "complaint",
                "apartment": c["apartmentID"],
                "issue": c["Description"],
                "date": c["reportDate"],
                "resolution": c["Resolution"]
            })

        for r in repairs:
            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": r["Notes"],
                "date": r["maintenanceDate"],
                "timeTaken": r["timeTaken"]
            })

        return requests


    @staticmethod
    def complete_request(db, request_id, request_type, time_taken, notes, cost):

        if request_type == "complaint":

            query = """
            UPDATE Complaint
            SET Status = 'closed',
                Resolution = %s
            WHERE complaintID = %s
            """

            db.execute(query, (notes, request_id))

        elif request_type == "repair":

            query = """
            UPDATE MaintenanceLog
            SET timeTaken = %s,
                Cost = %s,
                Notes = %s
            WHERE logID = %s
            """

            db.execute(query, (time_taken, cost, notes, request_id))
