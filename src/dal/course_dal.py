import pyodbc

class CourseDAL:
    def __init__(self, connection):
        self.connection = connection

    def get_all_courses(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Courses")
            courses = cursor.fetchall()
            return courses
        except pyodbc.Error as e:
            print("Error fetching courses:", e)
            return []

    def add_course(self, course_name, course_description):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Courses (Name, Description) VALUES (?, ?)", (course_name, course_description))
            self.connection.commit()
        except pyodbc.Error as e:
            print("Error adding course:", e)

    def update_course(self, course_id, course_name, course_description):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE Courses SET Name = ?, Description = ? WHERE Id = ?", (course_name, course_description, course_id))
            self.connection.commit()
        except pyodbc.Error as e:
            print("Error updating course:", e)

    def delete_course(self, course_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Courses WHERE Id = ?", (course_id,))
            self.connection.commit()
        except pyodbc.Error as e:
            print("Error deleting course:", e)