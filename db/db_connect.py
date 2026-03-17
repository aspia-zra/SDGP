import mysql.connector
from mysql.connector import errorcode

class Database:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root123456!",
            database="secondverparagonapartment"
        )

        # dictionary=True so rows return as {"column": value}
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()


# default shared connection (optional)
db = Database()
