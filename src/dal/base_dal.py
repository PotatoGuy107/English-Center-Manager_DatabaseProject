import pyodbc

class BaseDAL:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.connection_string)
            return self.connection
        except pyodbc.Error as e:
            print("Connection failed:", e)
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()