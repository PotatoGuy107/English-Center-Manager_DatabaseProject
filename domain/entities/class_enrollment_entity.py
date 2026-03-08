class ClassEnrollment:
    """ClassEnrollment entity matching SQL Server Class_Enrollment table"""
    def __init__(
        self,
        class_enrollment_id: int = None,
        student_id: int = None,
        class_id: int = None,
        join_date=None,
        status: str = "Active",
    ):
        self.class_enrollment_id = class_enrollment_id
        self.student_id = student_id
        self.class_id = class_id
        self.join_date = join_date
        self.status = status
