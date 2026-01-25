class Teacher:
    def __init__(self, teacher_id, first_name, last_name, subject):
        self.teacher_id = teacher_id
        self.first_name = first_name
        self.last_name = last_name
        self.subject = subject

    def __repr__(self):
        return f'Teacher({self.teacher_id}, {self.first_name}, {self.last_name}, {self.subject})'