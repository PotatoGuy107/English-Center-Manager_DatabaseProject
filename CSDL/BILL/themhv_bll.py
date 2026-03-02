from DAL.dshv_dal import FakeStudentRepository
from MODELS.student import Student
from PyQt6.QtCore import QDate


class themhvbll:
    def __init__(self):
        self.repo = FakeStudentRepository()

    def get_students_by_class(self, class_code):
        return self.repo.get_students_by_class(class_code)

    def search_students(self, class_code, keyword):
        return self.repo.search_students(class_code, keyword)

    def save_student(self, class_code, student_id, name,
                     birth, gender, address, phone, email):

        # Nếu đã tồn tại → update
        if student_id and self.repo.exists(student_id):
            return self.repo.update_student(student_id, name, phone, email)

        # Nếu chưa có → thêm mới
        new_id = self.repo.generate_student_id()

        new_student = Student(
            class_code,
            new_id,
            name,
            birth,
            gender,
            address,
            phone,
            email,
            QDate.currentDate()
        )

        self.repo.add_student(new_student)
        return new_id

    def delete_student(self, student_id):
        self.repo.delete_student(student_id)