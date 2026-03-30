# using 'maintenance log' from class diagram
# some functions in here actually make sense to go in the complaints class
# class diagram actually has to change to reflect the implemented functions

from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

class Repair:

    PRIORITY_MAP = {
        "low": "1",
        "medium": "2",
        "high": "3",
        "1": "1",
        "2": "2",
        "3": "3",
    }

    @staticmethod
    def _normalize_priority(priority):
        if priority is None:
            return None

        value = str(priority).strip().lower()
        return Repair.PRIORITY_MAP.get(value)

    @staticmethod
    def _format_date_only(value):
        if value is None:
            return "-"

        if isinstance(value, datetime):
            return value.strftime("%d-%m-%y")

        if isinstance(value, str):
            date_part = value.split(" ")[0].split("T")[0]
            for fmt in ("%Y-%m-%d", "%d-%m-%y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(date_part, fmt).strftime("%d-%m-%y")
                except ValueError:
                    continue
            return date_part

        return value

    @staticmethod
    def _decode_complaint_description(description, initial_issue=None):
        reason = (str(description or "").strip() or "-")
        details = (str(initial_issue or "").strip() or "-")
        return reason, details

    @staticmethod
    def _is_unknown_column_error(exc):
        message = str(exc).lower()
        return "unknown column" in message

    def __init__(self, apartmentID, logID=None, userID=None, maintenanceDate=None, timeTaken=None, Cost=None, Notes=None):
        self.logID = logID
        self.apartmentID = apartmentID
        self.userID = userID
        self.maintenanceDate = maintenanceDate
        self.timeTaken = timeTaken
        self.Cost = Cost
        self.Notes = Notes


    @staticmethod
    def log_maintenance(db, apartmentID, userID, maintenanceDate, issue=None, priority=None, repair_details=None):
        query = """
        INSERT INTO MaintenanceLog
        (apartmentID, userID, maintenanceDate, Priority, InitialIssue, RepairDetails)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        normalized_priority = Repair._normalize_priority(priority) or "2"
        issue_text = (issue or "").strip() or None
        details_text = (repair_details or "").strip() or None
        db.execute(
            query,
            (apartmentID, userID, maintenanceDate, normalized_priority, issue_text, details_text),
        )


    @staticmethod
    def calculate_total_cost(db, apartment_id):
        query = """
        SELECT SUM(Cost) AS total_cost
        FROM MaintenanceLog
        WHERE apartmentID=%s
        """
        result = db.fetch_one(query, (apartment_id,))
        return result.get("total_cost", 0) if result else 0


    @staticmethod
    def get_apartment_id_by_number(db, apartment_number):
        query = "SELECT apartmentID FROM Apartment WHERE apartmentNumber = %s"
        row = db.fetch_one(query, (apartment_number,))
        if not row:
            return None

        return row.get("apartmentID")


# Complaint helper functions


    @staticmethod
    def get_open_complaints(db):
        query = """
        SELECT complaintID, apartmentID, InitialIssue, Description, reportDate, Severity
        FROM Complaint
        WHERE Status = 'open'
        """
        fallback_query = """
        SELECT complaintID,
               apartmentID,
               Description AS InitialIssue,
               Description,
               reportDate,
               Severity
        FROM Complaint
        WHERE Status = 'open'
        """
        try:
            return db.fetch_all(query)
        except Exception as exc:
            if Repair._is_unknown_column_error(exc):
                return db.fetch_all(fallback_query)
            raise


    @staticmethod
    def get_closed_complaints(db):
        query = """
        SELECT complaintID, apartmentID, InitialIssue, Description, reportDate, FinalResolution, Severity
        FROM Complaint
        WHERE Status = 'closed'
        """
        fallback_query = """
        SELECT complaintID,
               apartmentID,
               Description AS InitialIssue,
               Description,
               reportDate,
               NULL AS FinalResolution,
               Severity
        FROM Complaint
        WHERE Status = 'closed'
        """
        try:
            return db.fetch_all(query)
        except Exception as exc:
            if Repair._is_unknown_column_error(exc):
                return db.fetch_all(fallback_query)
            raise


# -----------------------------
# Repair helper functions
# -----------------------------

    @staticmethod
    def get_open_repairs(db):
        query = """
        SELECT ml.logID,
               ml.apartmentID,
               ml.userID,
               u.fullName AS workerName,
               ml.maintenanceDate,
               ml.Priority,
               ml.InitialIssue,
               ml.RepairDetails
        FROM MaintenanceLog ml
        LEFT JOIN UserTbl u ON u.userID = ml.userID
        WHERE ml.timeTaken IS NULL
        """
        return db.fetch_all(query)


    @staticmethod
    def get_completed_repairs(db):
        query = """
        SELECT ml.logID,
               ml.apartmentID,
               ml.userID,
               u.fullName AS workerName,
               ml.maintenanceDate,
               ml.Priority,
               ml.InitialIssue,
               ml.RepairDetails,
               ml.FinalResolution,
               ml.timeTaken,
               ml.Cost
        FROM MaintenanceLog ml
        LEFT JOIN UserTbl u ON u.userID = ml.userID
        WHERE ml.timeTaken IS NOT NULL
        """
        return db.fetch_all(query)


# -----------------------------
# Dashboard request functions
# -----------------------------

    @staticmethod
    def get_openrequests(db):

        complaints = Repair.get_open_complaints(db)
        repairs = Repair.get_open_repairs(db)

        requests = []

        for c in complaints:
            complaint_reason, complaint_details = Repair._decode_complaint_description(c["Description"], c.get("InitialIssue"))
            requests.append({
                "id": c["complaintID"],
                "type": "complaint",
                "apartment": c["apartmentID"],
                "issue": complaint_reason,
                "complaintDetails": complaint_details,
                "date": Repair._format_date_only(c["reportDate"]),
                "worker": None,
                "priority": Repair._normalize_priority(c["Severity"])
            })

        for r in repairs:
            issue = (r.get("InitialIssue") or "").strip()
            priority = Repair._normalize_priority(r.get("Priority"))
            worker_name = str(r.get("workerName") or "").strip()
            worker_id = r.get("userID")
            worker_label = worker_name

            if not worker_label and worker_id is not None:
                worker_label = f"Worker #{worker_id}"

            if not worker_label:
                worker_label = "Unassigned"

            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": issue or "-",
                "repairDetails": (r.get("RepairDetails") or "-").strip(),
                "date": Repair._format_date_only(r["maintenanceDate"]),
                "worker": worker_label,
                "priority": Repair._normalize_priority(priority)
            })

        return requests


    @staticmethod
    def get_completed_requests(db):

        complaints = Repair.get_closed_complaints(db)
        repairs = Repair.get_completed_repairs(db)

        requests = []

        for c in complaints:
            complaint_reason, complaint_details = Repair._decode_complaint_description(c["Description"], c.get("InitialIssue"))
            requests.append({
                "id": c["complaintID"],
                "type": "complaint",
                "apartment": c["apartmentID"],
                "issue": complaint_reason,
                "complaintDetails": complaint_details,
                "date": Repair._format_date_only(c["reportDate"]),
                "priority": Repair._normalize_priority(c["Severity"]),
                "timeTaken": "-",
                "cost": "-",
                "resolution": c["FinalResolution"],
                "_sort_date": c["reportDate"],
            })

        for r in repairs:
            issue = (r.get("InitialIssue") or "").strip()
            priority = Repair._normalize_priority(r.get("Priority"))
            resolution_text = str(r.get("FinalResolution") or "-").strip() or "-"

            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": issue or "-",
                "repairDetails": (r.get("RepairDetails") or "-").strip(),
                "date": Repair._format_date_only(r["maintenanceDate"]),
                "priority": Repair._normalize_priority(priority),
                "timeTaken": r["timeTaken"],
                "cost": r["Cost"],
                "resolution": resolution_text,
                "_sort_date": r["maintenanceDate"],
            })

        requests.sort(
            key=lambda item: item.get("_sort_date") or datetime.min,
            reverse=True,
        )

        for item in requests:
            item.pop("_sort_date", None)

        return requests


    @staticmethod
    def complete_request(db, request_id, request_type, time_taken, notes, cost):

        if request_type == "complaint":

            query = """
            UPDATE Complaint
            SET Status = 'closed',
                FinalResolution = %s,
                reportDate = NOW()
            WHERE complaintID = %s
            """

            try:
                db.execute(query, (notes, request_id))
            except Exception as exc:
                if not Repair._is_unknown_column_error(exc):
                    raise

                fallback_query = """
                UPDATE Complaint
                SET Status = 'closed',
                    reportDate = NOW()
                WHERE complaintID = %s
                """
                db.execute(fallback_query, (request_id,))

        elif request_type == "repair":

            query = """
            UPDATE MaintenanceLog
            SET timeTaken = %s,
                Cost = %s,
                FinalResolution = %s
            WHERE logID = %s
            """

            db.execute(query, (time_taken, cost, notes, request_id))

    @staticmethod #khanh this is where i was trying to send tenants their booked repair notifications, you can change the next two functions completely or delete them for the banner
    def get_tenant_email_by_apartment(db, apartment_id):
        query = """
        SELECT t.Email
        FROM LeaseAgreement la
        JOIN Tenant t ON t.tenantID = la.tenantID
        WHERE la.apartmentID = %s
          AND la.Status = 'active'
        LIMIT 1
        """
        row = db.fetch_one(query, (apartment_id,))
        if not row:
            return None
        return row.get("Email")

    @staticmethod
    def send_maintenance_notification(db, apartment_id, scheduled_date):
        tenant_email = Repair.get_tenant_email_by_apartment(db, apartment_id)
        if not tenant_email:
            return False, "No active tenant email found for this apartment."

        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        if not smtp_user or not smtp_password:
            return False, "Email not configured. Set SMTP_USER and SMTP_PASSWORD environment variables."

        date_text = Repair._format_date_only(scheduled_date)
        body = (
            "Dear Tenant,\n\n"
            "Please be aware that a technician will be visiting your apartment to resolve "
            f"your maintenance request on {date_text}.\n\n"
            "Regards,\nParagon Apartments Management"
        )

        message = EmailMessage()
        message["Subject"] = "Maintenance Visit Notice"
        message["From"] = smtp_user
        message["To"] = tenant_email
        message.set_content(body)

        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as smtp:
                smtp.starttls()
                smtp.login(smtp_user, smtp_password)
                smtp.send_message(message)
            return True, f"Email notification sent to {tenant_email}."
        except Exception as exc:
            return False, f"Email send failed: {exc}"

