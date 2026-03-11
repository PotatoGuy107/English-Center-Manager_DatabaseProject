from dataclasses import dataclass
from PyQt6.QtCore import QDate
from infrastructure.repositories.class_repository import ClassRepository
from infrastructure.repositories.class_enrollment_repository import ClassEnrollmentRepository


@dataclass
class ClassListItem:
    """DTO for class list display"""
    code: str
    name: str
    course: str
    teacher: str
    start_date: QDate
    end_date: QDate
    progress: str
    status: str


class ClassListUseCases:
    def __init__(self):
        self.repo = ClassRepository()

    def get_all_classes(self) -> list:
        classes = self.repo.get_all_classes()
        result = []
        for c in classes:
            # c: (class_id, class_name, course_name, skill_name, teacher_id, start_date, end_date, max_student, status)
            class_id = c[0]
            class_name = c[1]
            course_name = c[2] or ""
            teacher_id = c[4]
            start_date = c[5]
            end_date = c[6]
            max_student = c[7] or 0
            status = c[8] or ""
            
            # Get teacher name
            from infrastructure.repositories.teacher_repository import TeacherRepository
            teacher = TeacherRepository.get_by_id(teacher_id) if teacher_id else None
            teacher_name = teacher[1] if teacher else ""
            
            # Convert dates to QDate
            if start_date:
                start_qdate = QDate(start_date.year, start_date.month, start_date.day)
            else:
                start_qdate = QDate.currentDate()
            
            if end_date:
                end_qdate = QDate(end_date.year, end_date.month, end_date.day)
            else:
                end_qdate = QDate.currentDate()
            
            # Get enrolled students count using ClassEnrollmentRepository
            enrolled = ClassEnrollmentRepository.get_by_class(class_id)
            progress = f"{len(enrolled)}/{max_student}"
            
            result.append(ClassListItem(
                code=str(class_id),
                name=class_name,
                course=course_name,
                teacher=teacher_name,
                start_date=start_qdate,
                end_date=end_qdate,
                progress=progress,
                status=status
            ))
        return result
