import pyodbc

class StudentDAL:
    def __init__(self, connection):
        self.connection = connection

    def get_all_students(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        cursor.close()
        return students

    def get_student_by_id(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        cursor.close()
        return student

    def add_student(self, student_data):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Students (name, age, email) VALUES (?, ?, ?)", 
                       (student_data['name'], student_data['age'], student_data['email']))
        self.connection.commit()
        cursor.close()

    def update_student(self, student_id, student_data):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Students SET name = ?, age = ?, email = ? WHERE id = ?", 
                       (student_data['name'], student_data['age'], student_data['email'], student_id))
        self.connection.commit()
        cursor.close()

    def delete_student(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Students WHERE id = ?", (student_id,))
        self.connection.commit()
        cursor.close()