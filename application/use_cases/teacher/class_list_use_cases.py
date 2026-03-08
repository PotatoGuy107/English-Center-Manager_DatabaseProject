from infrastructure.repositories.class_repository import ClassRepository


class TeacherClassListUseCases:
    def __init__(self):
        self.repo = ClassRepository()

    def get_all_classes(self) -> list:
        return self.repo.get_all_classes()
