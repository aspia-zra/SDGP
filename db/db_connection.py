import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="passeord",
        database="secondverparagonapartment"
    )

    return connection
