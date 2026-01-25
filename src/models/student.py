class Student:
    def __init__(self, student_id, first_name, last_name, email, phone):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"Student({self.student_id}, {self.first_name}, {self.last_name}, {self.email}, {self.phone})"

    # Additional methods for business logic can be added here