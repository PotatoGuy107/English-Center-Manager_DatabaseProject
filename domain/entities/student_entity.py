class Student:
    """Student entity matching SQL Server Student table"""
    def __init__(
        self,
        student_id: int = None,
        full_name: str = "",
        date_of_birth=None,
        gender: str = None,
        address: str = None,
        phone_number: str = None,
        email: str = None,
        register_date=None,
        status: str = "Active",
    ):
        self.student_id = student_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.register_date = register_date
        self.status = status
