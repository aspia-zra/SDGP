# # Contains connection, Contains execute_query()


# def getconnection():
#     class DummyConn:
#         def cursor(self):
#             return self
        
#         def execute(self, *args, **kwargs):
#             pass
        
#         def fetchall(self):
#             return []
        
#         def close(self):
#             pass
    
#     return DummyConn()




 # apparently it's meant to look like this: 
 
 import mysql.connector

def getconnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root123456!",
        database="yourdbname" # change i forgot what it was
    )