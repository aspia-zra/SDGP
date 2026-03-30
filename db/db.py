import mysql.connector

def getconnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="sdgpdump"
    )