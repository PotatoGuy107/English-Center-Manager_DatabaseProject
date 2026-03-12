from abc import ABC, abstractmethod


class ICourseRepository(ABC):
    @abstractmethod
    def get_all_courses(self) -> list:
        pass

    @abstractmethod
    def get_skills_by_course(self, course_id) -> list:
        pass

    @abstractmethod
    def insert_course(self, data) -> None:
        pass

    @abstractmethod
    def update_course(self, data) -> None:
        pass

    @abstractmethod
    def delete_course(self, course_id) -> None:
        pass
