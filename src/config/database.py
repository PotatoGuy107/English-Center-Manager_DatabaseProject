import pyodbc
from .database_config import DATABASE_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.server = DATABASE_CONFIG["host"]
        self.database = DATABASE_CONFIG["database"]
        self.uid = DATABASE_CONFIG["user"]
        self.pwd = DATABASE_CONFIG["password"]
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