from domain.entities.student_entity import Student
from domain.interfaces.i_student_repository import IStudentRepository
from PyQt6.QtCore import QDate


class StudentRepository(IStudentRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.students = [
                Student("L001", "HV001", "Nguyen Van A", QDate(2000, 1, 1), "Male", "Hanoi", "0901000001", "a@email.com", QDate.currentDate()),
                Student("L001", "HV002", "Tran Thi B", QDate(2001, 5, 15), "Female", "HCM", "0901000002", "b@email.com", QDate.currentDate()),
                Student("L002", "HV003", "Le Van C", QDate(1999, 9, 20), "Male", "Danang", "0901000003", "c@email.com", QDate.currentDate()),
            ]
            cls._instance.next_id = 4
        return cls._instance

    def get_students_by_class(self, class_code) -> list:
        return [s for s in self.students if s.class_code == class_code]

    def search_students(self, class_code, keyword) -> list:
        kw = keyword.lower()
        return [
            s for s in self.students
            if s.class_code == class_code and (kw in s.student_id.lower() or kw in s.name.lower())
        ]

    def add_student(self, student) -> None:
        self.students.append(student)
        self.next_id += 1

    def update_student(self, student_id, name, phone, email) -> bool:
        for s in self.students:
            if s.student_id == student_id:
                s.name = name
                s.phone = phone
                s.email = email
                return True
        return False

    def delete_student(self, student_id) -> bool:
        before = len(self.students)
        self.students = [s for s in self.students if s.student_id != student_id]
        return len(self.students) < before

    def exists(self, student_id) -> bool:
        return any(s.student_id == student_id for s in self.students)

    def generate_student_id(self) -> str:
        max_num = 0
        for s in self.students:
            try:
                num = int(s.student_id.replace("HV", ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
        return f"HV{max_num + 1:03d}"
