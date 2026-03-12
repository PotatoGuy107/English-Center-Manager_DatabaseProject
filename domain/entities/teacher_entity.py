class Teacher:
    """Teacher entity matching SQL Server Teacher table"""
    def __init__(
        self,
        teacher_id: int = None,
        full_name: str = "",
        phone_number: str = None,
        email: str = None,
        specialization: str = None,
        hire_date=None,
        status: str = "Active",
    ):
        self.teacher_id = teacher_id
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.specialization = specialization
        self.hire_date = hire_date
        self.status = status
