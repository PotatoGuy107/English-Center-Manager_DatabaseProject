# models/schedule_model.py

from PyQt6.QtCore import QDate


class ScheduleModel:
    def __init__(self, class_code, date: QDate, ca, room, teacher):
        self.class_code = class_code
        self.date = date
        self.ca = ca
        self.room = room
        self.teacher = teacher
