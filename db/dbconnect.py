import mysql.connector
from mysql.connector import errorcode

hostname = "localhost"
db = "SDGPDUMP"
username = "root"
passwd = "Root123456!"


def get_connection():
    try:
        conn = mysql.connector.connect(
                host=hostname,
                user=username,
                password=passwd,
                database=db
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

def cursor():
    conn = get_connection()
    if conn:
        return conn.cursor()
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
