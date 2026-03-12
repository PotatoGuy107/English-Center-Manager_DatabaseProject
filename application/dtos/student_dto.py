from dataclasses import dataclass


@dataclass
class StudentDTO:
    student_id: str
    name: str
    phone: str
    email: str
