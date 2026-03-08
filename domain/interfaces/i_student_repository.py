from abc import ABC, abstractmethod


class IStudentRepository(ABC):
    @abstractmethod
    def get_students_by_class(self, class_code) -> list:
        pass

    @abstractmethod
    def search_students(self, class_code, keyword) -> list:
        pass

    @abstractmethod
    def add_student(self, student) -> None:
        pass

    @abstractmethod
    def update_student(self, student_id, name, phone, email) -> bool:
        pass

    @abstractmethod
    def delete_student(self, student_id) -> bool:
        pass

    @abstractmethod
    def exists(self, student_id) -> bool:
        pass

    @abstractmethod
    def generate_student_id(self) -> str:
        pass
