import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mire6374*",
        database="secondverparagonapartment"
    )

def getconnection():
    return get_connection()