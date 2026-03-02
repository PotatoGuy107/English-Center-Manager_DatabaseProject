from DAL.dshv_dal import FakeStudentRepository


class DSHocVienBLL:

    def __init__(self):
        self.repo = FakeStudentRepository()

    def get_students_by_class(self, class_code):
        return self.repo.get_students_by_class(class_code)

    def search_students(self, class_code, keyword):
        return self.repo.search_students(class_code, keyword)

    def update_student(self, student_id, name, phone, email):
        return self.repo.update_student(student_id, name, phone, email)
    
    @staticmethod
    def validate_student(name, phone, email):

        if not name.strip():
            return False, "Tên không được để trống"

        if not phone.strip():
            return False, "SĐT không được để trống"

        if not phone.isdigit():
            return False, "SĐT phải là số"

        if len(phone) < 9:
            return False, "SĐT không hợp lệ"

        if not email.strip():
            return False, "Email không được để trống"

        if "@" not in email:
            return False, "Email không hợp lệ"

        return True, ""
