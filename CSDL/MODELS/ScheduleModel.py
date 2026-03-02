# models/schedule_model.py

from PyQt6.QtCore import QDate



class ScheduleModel:
    def __init__(
        self,
        class_code,
        start_date,
        end_date,
        weekday,
        ca,
        room,
        teacher
    ):
        self.class_code = class_code
        self.start_date = start_date
        self.end_date = end_date
        self.weekday = weekday
        self.ca = ca
        self.room = room
        self.teacher = teacher
