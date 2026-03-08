from domain.entities.student_entity import Student
from infrastructure.repositories.student_repository import StudentRepository
from PyQt6.QtCore import QDate


class AddStudentUseCases:
    def __init__(self):
        self.repo = StudentRepository()

    def get_students_by_class(self, class_code) -> list:
        return self.repo.get_students_by_class(class_code)

    def search_students(self, class_code, keyword) -> list:
        return self.repo.search_students(class_code, keyword)

    def save_student(
        self, class_code, student_id, name, birth, gender, address, phone, email
    ):
        if self.repo.exists(student_id):
            self.repo.update_student(student_id, name, phone, email)
            return student_id
        new_id = self.repo.generate_student_id()
        student = Student(
            class_code,
            new_id,
            name,
            birth,
            gender,
            address,
            phone,
            email,
            QDate.currentDate(),
        )
        self.repo.add_student(student)
        return new_id

    def delete_student(self, student_id) -> bool:
        return self.repo.delete_student(student_id)
