import mysql.connector
from mysql.connector import errorcode

class Database:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root123456!",
            database="SDGPDUMP"
        )

        # Buffered cursor prevents "Unread result found" across back-to-back queries.
        self.cursor = self.conn.cursor(dictionary=True, buffered=True)

    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values)
        row = self.cursor.fetchone()
        # Drain any remaining rows so the next execute never sees unread results.
        self.cursor.fetchall()
        return row

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()


# default shared connection (optional)
db = Database()
