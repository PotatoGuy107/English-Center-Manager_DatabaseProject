class Course:
    """Course entity matching SQL Server Course table"""
    def __init__(
        self,
        course_id: int = None,
        course_name: str = "",
        description: str = None,
        level: str = None,
        duration_weeks: int = None,
        tuition_fee: float = None,
        status: str = "Active",
    ):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.level = level
        self.duration_weeks = duration_weeks
        self.tuition_fee = tuition_fee
        self.status = status
