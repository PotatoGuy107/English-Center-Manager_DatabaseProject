from infrastructure.repositories.class_repository import ClassRepository
from infrastructure.repositories.student_repository import StudentRepository


class ClassListUseCases:
    def __init__(self):
        self.repo = ClassRepository()
        self.student_repo = StudentRepository()

    def get_all_classes(self) -> list:
        classes = self.repo.get_all_classes()
        for c in classes:
            enrolled = self.student_repo.get_students_by_class(c.code)
            c.progress = f"{len(enrolled)}/{c.max_students}"
        return classes
