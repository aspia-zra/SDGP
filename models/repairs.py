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
    def _encode_notes(issue, priority):
        issue_text = (issue or "").strip()
        priority_text = Repair._normalize_priority(priority)

        if issue_text and priority_text:
            return f"[Priority:{priority_text}] {issue_text}"

        return issue_text or None

    @staticmethod
    def _decode_notes(notes):
        if not notes:
            return "-", None

        def reason_only(value):
            return (str(value or "-").splitlines()[0].strip() or "-")

        text = str(notes).strip()
        if text.startswith("[Priority:") and "]" in text:
            closing = text.find("]")
            priority = Repair._normalize_priority(text[len("[Priority:"):closing].strip())
            issue = text[closing + 1:].strip() or "-"
            marker = "[Resolution]"
            if marker in issue:
                issue = issue[:issue.find(marker)].rstrip() or "-"
            return reason_only(issue), priority

        marker = "[Resolution]"
        if marker in text:
            text = text[:text.find(marker)].rstrip() or "-"

        return reason_only(text), None

    @staticmethod
    def _extract_resolution(notes):
        if not notes:
            return None

        marker = "[Resolution]"
        text = str(notes)
        idx = text.find(marker)
        if idx == -1:
            return None

        return text[idx + len(marker):].strip() or None

    @staticmethod
    def _merge_resolution(existing_notes, resolution):
        base = (existing_notes or "").strip()
        resolution_text = (resolution or "").strip()

        if not resolution_text:
            return base or None

        marker = "[Resolution]"
        if marker in base:
            base = base[:base.find(marker)].rstrip()

        if not base:
            return f"{marker} {resolution_text}"

        return f"{base}\n{marker} {resolution_text}"

    @staticmethod
    def _decode_complaint_description(description):
        text = str(description or "").strip()
        if not text:
            return "-", "-"

        reason_marker = "[Reason]"
        details_marker = "[Details]"

        if reason_marker in text and details_marker in text:
            reason_start = text.find(reason_marker) + len(reason_marker)
            details_start = text.find(details_marker)
            reason = text[reason_start:details_start].strip() or "-"
            details = text[details_start + len(details_marker):].strip() or "-"
            return reason, details

        reason = text.splitlines()[0].strip() if text else "-"
        return reason or "-", text

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
        (apartmentID, userID, maintenanceDate, Priority, InitialIssue, RepairDetails, Notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        normalized_priority = Repair._normalize_priority(priority) or "2"
        issue_text = (issue or "").strip() or None
        details_text = (repair_details or "").strip() or None
        db.execute(
            query,
            (apartmentID, userID, maintenanceDate, normalized_priority, issue_text, details_text, details_text),
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
        SELECT COUNT(*) AS worker_count
        FROM MaintenanceLog
        WHERE userID = %s AND DATE(maintenanceDate) = DATE(%s)
        """
        result = db.fetch_one(query, (user_id, date))
        return result.get("worker_count", 0) == 0


    @staticmethod
    def check_role(db, user_id, required_role="maintenance"):
        query = "SELECT Role FROM UserTbl WHERE userID = %s"
        role = db.fetch_one(query, (user_id,))

        if role is None:
            return False

        return role.get("Role") == required_role



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
        SELECT complaintID, apartmentID, Description, reportDate, Resolution, Severity
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
        SELECT logID, apartmentID, userID, maintenanceDate, Priority, InitialIssue, RepairDetails, Notes
        FROM MaintenanceLog
        WHERE timeTaken IS NULL
        """
        return db.fetch_all(query)


    @staticmethod
    def get_completed_repairs(db):
        query = """
        SELECT logID, apartmentID, userID, maintenanceDate, Priority, InitialIssue, RepairDetails, FinalResolution, timeTaken, Cost, Notes
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
            FinalResolution = %s,
            maintenanceDate = NOW()
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
            complaint_reason, complaint_details = Repair._decode_complaint_description(c["Description"])
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

            if not issue:
                issue, decoded_priority = Repair._decode_notes(r.get("Notes"))
                priority = priority or decoded_priority

            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": issue,
                "repairDetails": (r.get("RepairDetails") or r.get("Notes") or "-").strip(),
                "date": Repair._format_date_only(r["maintenanceDate"]),
                "worker": r["userID"],
                "priority": Repair._normalize_priority(priority)
            })

        return requests


    @staticmethod
    def get_completed_requests(db):

        complaints = Repair.get_closed_complaints(db)
        repairs = Repair.get_completed_repairs(db)

        requests = []

        for c in complaints:
            complaint_reason, complaint_details = Repair._decode_complaint_description(c["Description"])
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
                "resolution": c["Resolution"],
                "_sort_date": c["reportDate"],
            })

        for r in repairs:
            issue = (r.get("InitialIssue") or "").strip()
            priority = Repair._normalize_priority(r.get("Priority"))

            if not issue:
                issue, decoded_priority = Repair._decode_notes(r.get("Notes"))
                priority = priority or decoded_priority

            requests.append({
                "id": r["logID"],
                "type": "repair",
                "apartment": r["apartmentID"],
                "issue": issue,
                "repairDetails": (r.get("RepairDetails") or r.get("Notes") or "-").strip(),
                "date": Repair._format_date_only(r["maintenanceDate"]),
                "priority": Repair._normalize_priority(priority),
                "timeTaken": r["timeTaken"],
                "cost": r["Cost"],
                "resolution": (r.get("FinalResolution") or Repair._extract_resolution(r.get("Notes")) or "-").strip(),
                "_sort_date": r["maintenanceDate"],
            })

        requests.sort(
            key=lambda item: item.get("_sort_date") or datetime.min,
            reverse=True,
        )

        limited_requests = requests[:5]
        for item in limited_requests:
            item.pop("_sort_date", None)

        return limited_requests


    @staticmethod
    def complete_request(db, request_id, request_type, time_taken, notes, cost):

        if request_type == "complaint":

            query = """
            UPDATE Complaint
            SET Status = 'closed',
                Resolution = %s,
                reportDate = NOW()
            WHERE complaintID = %s
            """

            db.execute(query, (notes, request_id))

        elif request_type == "repair":

            query = """
            UPDATE MaintenanceLog
            SET timeTaken = %s,
                Cost = %s,
                FinalResolution = %s,
                maintenanceDate = NOW()
            WHERE logID = %s
            """

            db.execute(query, (time_taken, cost, notes, request_id))

    @staticmethod
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

        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        sender_email = os.getenv("SMTP_FROM", smtp_user)

        if not smtp_host or not sender_email:
            return False, "SMTP is not configured. Set SMTP_HOST and SMTP_USER/SMTP_FROM."

        date_text = Repair._format_date_only(scheduled_date)
        body = (
            "Please be aware that a technician/worker will be resolving your issue on "
            f"{date_text}."
        )

        message = EmailMessage()
        message["Subject"] = "Maintenance Visit Notice"
        message["From"] = sender_email
        message["To"] = tenant_email
        message.set_content(body)

        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
                smtp.starttls()
                if smtp_user and smtp_password:
                    smtp.login(smtp_user, smtp_password)
                smtp.send_message(message)

            return True, f"Email notification sent to {tenant_email}."
        except Exception as exc:
            return False, f"Email send failed: {exc}"
