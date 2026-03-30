import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mire6374*",
        database='secondverparagonapartment'
    )
    return connection
