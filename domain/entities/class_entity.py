from PyQt6.QtCore import QDate


class Class:
    def __init__(
        self,
        code,
        name,
        course,
        skill,
        teacher,
        start_date: QDate,
        end_date: QDate,
        max_students: int,
        status="Sắp khai giảng",
        progress=None,
    ):
        self.code = code
        self.name = name
        self.course = course
        self.skill = skill
        self.teacher = teacher
        self.start_date = start_date
        self.end_date = end_date
        self.max_students = max_students
        self.status = status
        self.progress = progress
