class Enrollment:
    """Enrollment entity matching SQL Server Enrollment table"""
    def __init__(
        self,
        enrollment_id: int = None,
        student_id: int = None,
        course_id: int = None,
        enrollment_date=None,
        start_date=None,
        end_date=None,
        enrollment_status: str = "Active",
    ):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.start_date = start_date
        self.end_date = end_date
        self.enrollment_status = enrollment_status
