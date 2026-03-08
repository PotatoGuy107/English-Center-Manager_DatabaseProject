from infrastructure.repositories.student_repository import StudentRepository


class StudentUseCases:
    def __init__(self):
        self.repo = StudentRepository()

    def get_students_by_class(self, class_code) -> list:
        return self.repo.get_students_by_class(class_code)

    def search_students(self, class_code, keyword) -> list:
        return self.repo.search_students(class_code, keyword)

    def update_student(self, student_id, name, phone, email) -> bool:
        return self.repo.update_student(student_id, name, phone, email)

    @staticmethod
    def validate_student(name, phone, email) -> tuple[bool, str]:
        if not name or not name.strip():
            return False, "Name is required"
        if not phone or not phone.strip():
            return False, "Phone is required"
        if not phone.strip().isdigit() or len(phone.strip()) < 9:
            return False, "Phone must be numeric and at least 9 digits"
        if not email or not email.strip():
            return False, "Email is required"
        if "@" not in email:
            return False, "Invalid email address"
        return True, ""
