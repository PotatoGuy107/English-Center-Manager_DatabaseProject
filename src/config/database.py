import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, uid, pwd):
        self.server = server
        self.database = database
        self.uid = uid
        self.pwd = pwd
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.uid};PWD={self.pwd}'
            )
            return self.connection
        except pyodbc.Error as e:
            print("Connection failed:", e)
            return None