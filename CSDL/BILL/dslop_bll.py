from DAL.class_dal import ClassDAL
from DAL.dshv_dal import FakeStudentRepository

class DSLopBLL:
    def __init__(self):
        self.repo = ClassDAL()
        self.student_repo = FakeStudentRepository()

    def get_all_classes(self):
        classes = self.repo.get_all_classes()

        for c in classes:
            students = self.student_repo.get_students_by_class(c.code)
            current = len(students)
            c.progress = f"{current}/{c.max_class}"

        return classes