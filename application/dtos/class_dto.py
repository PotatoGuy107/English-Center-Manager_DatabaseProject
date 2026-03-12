from dataclasses import dataclass
from PyQt6.QtCore import QDate


@dataclass
class ClassDTO:
    name: str
    course: str
    skill: str
    teacher: str
    start_date: QDate
    end_date: QDate
    max_students: int
