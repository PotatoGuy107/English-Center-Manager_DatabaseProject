from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from infrastructure.repositories.exam_repository import ExamRepository


@dataclass
class ExamItem:
    """Data transfer object for exam display."""
    exam_id: int
    class_id: int
    class_name: str
    exam_type: str
    exam_date: date
    description: str


class ExamUseCases:
    """Use cases for exam management."""

    @staticmethod
    def get_all_exams() -> List[ExamItem]:
        """Get all exams with class names."""
        rows = ExamRepository.get_all()
        result = []
        for row in rows:
            exam_date = row[4]
            if isinstance(exam_date, str):
                from datetime import datetime
                exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
            
            result.append(ExamItem(
                exam_id=row[0],
                class_id=row[1],
                class_name=row[2] or "",
                exam_type=row[3] or "",
                exam_date=exam_date,
                description=row[5] or ""
            ))
        return result

    @staticmethod
    def get_exams_by_class(class_id: int) -> List[ExamItem]:
        """Get all exams for a specific class.
        
        get_by_class returns: (exam_id, exam_type, exam_date, description)
        """
        rows = ExamRepository.get_by_class(class_id)
        result = []
        for row in rows:
            exam_date = row[2]  # exam_date is at index 2
            if isinstance(exam_date, str):
                from datetime import datetime
                exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
            
            result.append(ExamItem(
                exam_id=row[0],
                class_id=class_id,
                class_name="",  # Not included in get_by_class
                exam_type=row[1] or "",
                exam_date=exam_date,
                description=row[3] or ""  # description is at index 3
            ))
        return result

    @staticmethod
    def create_exam(class_id: int, exam_type: str, exam_date: str, description: str) -> int:
        """Create a new exam. Returns the new exam_id."""
        exam_data = (class_id, exam_type, exam_date, description)
        return ExamRepository.insert(exam_data)

    @staticmethod
    def update_exam(exam_id: int, class_id: int, exam_type: str, exam_date: str, description: str) -> bool:
        """Update an existing exam.
        
        Repository expects: (exam_id, class_id, exam_type, exam_date, description)
        """
        exam_data = (exam_id, class_id, exam_type, exam_date, description)
        return ExamRepository.update(exam_data)

    @staticmethod
    def delete_exam(exam_id: int) -> bool:
        """Delete an exam by ID."""
        return ExamRepository.delete(exam_id)

    @staticmethod
    def get_exam_by_id(exam_id: int) -> Optional[ExamItem]:
        """Get a single exam by ID.
        
        get_by_id returns: (exam_id, class_id, exam_type, exam_date, description)
        """
        row = ExamRepository.get_by_id(exam_id)
        if not row:
            return None
        
        exam_date = row[3]  # exam_date is at index 3
        if isinstance(exam_date, str):
            from datetime import datetime
            exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
        
        return ExamItem(
            exam_id=row[0],
            class_id=row[1],
            class_name="",  # Not included in get_by_id
            exam_type=row[2] or "",
            exam_date=exam_date,
            description=row[4] or ""
        )
