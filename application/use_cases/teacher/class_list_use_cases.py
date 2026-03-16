from infrastructure.repositories.class_repository import ClassRepository


class TeacherClassListUseCases:
    def __init__(self):
        self.repo = ClassRepository()

    def get_all_classes(self) -> list:
        return self.repo.get_all_classes()

    def get_classes_by_teacher(self, teacher_id: str) -> list:
        """Get classes assigned to a specific teacher"""
        return self.repo.get_classes_by_teacher(teacher_id)

    def get_student_count(self, class_id: int) -> int:
        """Get enrolled student count for a class"""
        return self.repo.get_student_count_by_class(class_id)
