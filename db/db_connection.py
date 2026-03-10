import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mathsmasters1!",
        database="secondverparagonapartment"
    )

    return connection
