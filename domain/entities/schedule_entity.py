from PyQt6.QtCore import QDate


class Schedule:
    def __init__(
        self,
        class_code,
        start_date,
        end_date,
        weekday,
        shift,
        room,
        teacher,
    ):
        self.class_code = class_code
        self.start_date = start_date
        self.end_date = end_date
        self.weekday = weekday
        self.shift = shift
        self.room = room
        self.teacher = teacher
