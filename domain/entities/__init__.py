"""Domain entities matching SQL Server database schema"""

from .student_entity import Student
from .teacher_entity import Teacher
from .course_entity import Course
from .class_entity import Class
from .room_entity import Room
from .schedule_entity import Schedule
from .skill_entity import Skill
from .enrollment_entity import Enrollment
from .class_enrollment_entity import ClassEnrollment
from .exam_entity import Exam
from .exam_result_entity import ExamResult, ExamResultDetailed
from .payment_entity import Payment
from .score_entity import Score

__all__ = [
    "Student",
    "Teacher",
    "Course",
    "Class",
    "Room",
    "Schedule",
    "Skill",
    "Enrollment",
    "ClassEnrollment",
    "Exam",
    "ExamResult",
    "ExamResultDetailed",
    "Payment",
    "Score",
]