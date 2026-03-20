from unittest import result

import mysql.connector
from mysql.connector import errorcode

class Database:
    def __init__(self):
        self.hostname = "localhost"
        self.db = "secondverparagonapartment"
        self.username = "root"
        self.passwd = "Drashtisamgi02!"

        self.conn = self.get_connection()
        # if self.conn:
        #     print("Database connected successfully!")
        # else:
        #     print("Database connection failed!")

    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.hostname,
                user=self.username,
                password=self.passwd,
                database=self.db
            )
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Username or password is incorrect')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exist')
            else:
                print('Connection error:', err)
            return None

    def cursor(self):
        if self.conn:
            return self.conn.cursor()
        else:
            raise Exception("No database connection")

    def commit(self):
        if self.conn:
            self.conn.commit()
    
    def execute(self, query, values=None):
        cur = self.cursor()
        cur.execute(query, values or ())
        self.conn.commit()
        cur.close()

    def fetch_one(self, query, values=None):
        cur = self.cursor()
        cur.execute(query, values or ())
        result = cur.fetchone()
        cur.close()
        return result

    def fetch_all(self, query, values=None):
        cur = self.cursor()
        cur.execute(query, values or ())
        result = cur.fetchall()
        cur.close()
        return result
