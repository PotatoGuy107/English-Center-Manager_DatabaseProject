from MODELS.ScheduleModel import ScheduleModel
from PyQt6.QtCore import QDate


class FakeClassRepository:

    def __init__(self):
        self.schedules = [
            ScheduleModel("L001", QDate(2026, 5, 1), "Ca 1", "101", "GV A"),
            ScheduleModel("L002", QDate(2026, 5, 2), "Ca 2", "102", "GV B"),
        ]

    def insert_schedule(self, schedule):
        self.schedules.append(schedule)

    def get_schedules(self):
        return self.schedules

    def count_schedules_by_class(self, class_code):
        return sum(1 for s in self.schedules if s.class_code == class_code)
