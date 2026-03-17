# Contains connection, Contains execute_query()


def getconnection():
    class DummyConn:
        def cursor(self):
            return self
        
        def execute(self, *args, **kwargs):
            pass
        
        def fetchall(self):
            return []
        
        def close(self):
            pass
    
    return DummyConn()