from domain.entities.class_entity import Class
from domain.entities.schedule_entity import Schedule
from domain.interfaces.i_class_repository import IClassRepository
from PyQt6.QtCore import QDate


class ClassRepository(IClassRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.classes = [
                Class(
                    "L001",
                    "Lớp Mẫu",
                    "English Communication",
                    "Listening",
                    "T001",
                    QDate(2024, 1, 1),
                    QDate(2024, 6, 30),
                    20,
                    "Sắp khai giảng",
                )
            ]
            cls._instance.schedules = []
        return cls._instance

    def get_all_classes(self) -> list:
        return self.classes

    def get_last_class_code(self) -> str | None:
        if not self.classes:
            return None
        return self.classes[-1].code

    def insert_class(self, class_obj) -> tuple[bool, str]:
        for c in self.classes:
            if c.code == class_obj.code:
                return False, f"Class code {class_obj.code} already exists"
        self.classes.append(class_obj)
        return True, "Success"

    def get_all_schedules(self) -> list:
        return self.schedules

    def insert_schedules(self, schedule_list) -> bool:
        self.schedules.extend(schedule_list)
        return True

    def get_schedules_by_class(self, class_code) -> list:
        return [s for s in self.schedules if s.class_code == class_code]

    def delete_schedule_item(self, class_code, weekday, shift) -> bool:
        before = len(self.schedules)
        self.schedules = [
            s for s in self.schedules
            if not (s.class_code == class_code and s.weekday == weekday and s.shift == shift)
        ]
        return len(self.schedules) < before
