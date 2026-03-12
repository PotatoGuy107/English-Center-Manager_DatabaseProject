from infrastructure.repositories.student_db_repository import StudentDbRepository
from infrastructure.repositories.class_enrollment_repository import ClassEnrollmentRepository
from datetime import date


class AddStudentUseCases:
    def __init__(self):
        self.repo = StudentDbRepository()
        self.enrollment_repo = ClassEnrollmentRepository()

    def get_students_by_class(self, class_id) -> list:
        return self.repo.get_students_by_class(class_id)

    def search_students(self, class_id, keyword) -> list:
        # Search all students, then filter by class enrollment
        all_students = self.repo.search_students(keyword)
        return all_students

    def _format_date(self, date_obj) -> str:
        """Convert QDate or date object to SQL Server format yyyy-MM-dd"""
        if hasattr(date_obj, 'toString'):
            return date_obj.toString("yyyy-MM-dd")
        elif hasattr(date_obj, 'strftime'):
            return date_obj.strftime("%Y-%m-%d")
        return str(date_obj)

    def save_student(
        self, class_id, student_id, name, birth, gender, address, phone, email
    ):
        # Format date for SQL Server
        birth_str = self._format_date(birth) if birth else None
        today_str = date.today().strftime("%Y-%m-%d")
        
        existing = self.repo.get_student_by_id(student_id) if student_id else None
        
        if existing:
            # Update existing student
            update_data = (student_id, name, birth_str, gender, address, phone, email, "Active")
            self.repo.update_student(update_data)
            return student_id
        else:
            # Generate new student_id
            new_student_id = StudentDbRepository.get_next_student_id()
            
            # Insert new student: (student_id, full_name, date_of_birth, gender, address, phone_number, email, register_date, status)
            insert_data = (new_student_id, name, birth_str, gender, address, phone, email, today_str, "Active")
            self.repo.insert_student(insert_data)
            
            # Enroll student in class
            if class_id:
                enroll_id = ClassEnrollmentRepository.get_next_class_enrollment_id()
                enroll_data = (enroll_id, new_student_id, class_id, today_str, "Studying")
                self.enrollment_repo.insert(enroll_data)
            
            return new_student_id

    def delete_student(self, student_id) -> bool:
        try:
            self.repo.delete_student(student_id)
            return True
        except Exception:
            return False
