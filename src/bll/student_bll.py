class StudentBLL:
    def __init__(self, student_dal):
        self.student_dal = student_dal

    def add_student(self, student_data):
        # Logic to add a student
        return self.student_dal.insert_student(student_data)

    def update_student(self, student_id, student_data):
        # Logic to update a student
        return self.student_dal.update_student(student_id, student_data)

    def delete_student(self, student_id):
        # Logic to delete a student
        return self.student_dal.delete_student(student_id)

    def get_student(self, student_id):
        # Logic to retrieve a student
        return self.student_dal.get_student(student_id)

    def get_all_students(self):
        # Logic to retrieve all students
        return self.student_dal.get_all_students()