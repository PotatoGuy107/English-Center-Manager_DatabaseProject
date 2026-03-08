from abc import ABC, abstractmethod


class ITeacherRepository(ABC):
    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def insert(self, data) -> None:
        pass

    @abstractmethod
    def update(self, data) -> None:
        pass

    @abstractmethod
    def delete(self, teacher_id) -> None:
        pass
