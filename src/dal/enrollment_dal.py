import pyodbc
from config.database import DatabaseConnection

class EnrollmentDAL:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def add_enrollment(self, student_id, course_id):
        try:
            connection = self.db_connection.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Enrollments (StudentID, CourseID) VALUES (?, ?)", (student_id, course_id))
                connection.commit()
                cursor.close()
                return True
            return False
        except pyodbc.Error as e:
            print("Error adding enrollment:", e)
            return False

    def get_enrollments(self):
        try:
            connection = self.db_connection.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Enrollments")
                enrollments = cursor.fetchall()
                cursor.close()
                return enrollments
            return []
        except pyodbc.Error as e:
            print("Error fetching enrollments:", e)
            return []