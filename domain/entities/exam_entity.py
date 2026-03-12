class Exam:
    """Exam entity matching SQL Server Exam table"""
    def __init__(
        self,
        exam_id: int = None,
        class_id: int = None,
        exam_type: str = None,
        exam_date=None,
        description: str = None,
    ):
        self.exam_id = exam_id
        self.class_id = class_id
        self.exam_type = exam_type
        self.exam_date = exam_date
        self.description = description
