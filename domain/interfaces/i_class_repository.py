from abc import ABC, abstractmethod


class IClassRepository(ABC):
    @abstractmethod
    def get_all_classes(self) -> list:
        pass

    @abstractmethod
    def get_last_class_code(self) -> str | None:
        pass

    @abstractmethod
    def insert_class(self, class_obj) -> tuple[bool, str]:
        pass

    @abstractmethod
    def get_all_schedules(self) -> list:
        pass

    @abstractmethod
    def insert_schedules(self, schedule_list) -> bool:
        pass

    @abstractmethod
    def get_schedules_by_class(self, class_code) -> list:
        pass

    @abstractmethod
    def delete_schedule_item(self, class_code, weekday, shift) -> bool:
        pass
