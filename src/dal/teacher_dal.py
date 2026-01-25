from src.data.db_connection import DatabaseConnection

class TeacherDAL:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def get_all_teachers(self):
        connection = self.db_connection.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Teachers")
            teachers = cursor.fetchall()
            cursor.close()
            return teachers
        return []

    def add_teacher(self, teacher_data):
        connection = self.db_connection.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Teachers (name, subject) VALUES (?, ?)", 
                           (teacher_data['name'], teacher_data['subject']))
            connection.commit()
            cursor.close()

    def update_teacher(self, teacher_id, teacher_data):
        connection = self.db_connection.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Teachers SET name = ?, subject = ? WHERE id = ?", 
                           (teacher_data['name'], teacher_data['subject'], teacher_id))
            connection.commit()
            cursor.close()

    def delete_teacher(self, teacher_id):
        connection = self.db_connection.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Teachers WHERE id = ?", (teacher_id,))
            connection.commit()
            cursor.close()