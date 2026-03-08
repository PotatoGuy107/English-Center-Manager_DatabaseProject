class Class:
    """Class entity matching SQL Server Class table"""
    def __init__(
        self,
        class_id: int = None,
        skill_id: int = None,
        teacher_id: int = None,
        class_name: str = "",
        start_date=None,
        end_date=None,
        max_student: int = None,
        status: str = "Active",
    ):
        self.class_id = class_id
        self.skill_id = skill_id
        self.teacher_id = teacher_id
        self.class_name = class_name
        self.start_date = start_date
        self.end_date = end_date
        self.max_student = max_student
        self.status = status
