# admindashBE.py
from db import db
import mysql.connector
# from . import user_session
# import time, datetime

class mngBE():# values = ["All Roles", "Front-desk Staff", "Maintenance", "Finance"]
    @staticmethod
    def getAptData(): 
    
        # tableColumns = ("Apartment", "City", "Lease End", "Rent", "Status")
        conn = db.getconnection()
        cursor = conn.cursor()

        cursor.execute("""
                        SELECT 
                            a.apartmentNumber, 
                            l.City,
                            a.monthlyRent,
                            a.Status,
                            lease.endDate
                        FROM Apartment a
                        JOIN Location l
                            ON a.locationID = l.locationID
                        LEFT JOIN LeaseAgreement lease
                            ON a.apartmentID = lease.apartmentID
                        ORDER BY a.apartmentNumber
                     """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data # back to FE table
    @staticmethod
    def addApt(apartmentNumber, monthlyRent, status, city, aptType=None, address="TBD"):
        conn = db.getconnection()
        cursor = conn.cursor()
        try:
            normalized_status = status.lower()

            # insert city into Location
            cursor.execute(
                "INSERT INTO Location (City, Address) VALUES (%s, %s)",
                (city, address)
            )
            locationID = cursor.lastrowid

            # insert apartment
            cursor.execute(
                """
                INSERT INTO Apartment (apartmentNumber, locationID, monthlyRent, Status, Type)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (apartmentNumber, locationID, monthlyRent, normalized_status, aptType)
            )
            conn.commit()
        except mysql.connector.IntegrityError as e:
            conn.rollback()
            if e.errno == 1062:
                raise ValueError("Apartment number already exists") from e
            raise
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()