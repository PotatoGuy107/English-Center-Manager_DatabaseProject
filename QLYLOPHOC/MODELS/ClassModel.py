# models/class_model.py

from PyQt6.QtCore import QDate


class ClassModel:
    def __init__(self, code, name, course, skill, teacher, start_date: QDate, end_date: QDate, max_class: int):
        self.code = code
        self.name = name
        self.course = course
        self.skill = skill
        self.teacher = teacher
        self.start_date = start_date
        self.end_date = end_date
        self.max_class = max_class

