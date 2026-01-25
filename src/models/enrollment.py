class Enrollment:
    def __init__(self, student_id, course_id, enrollment_date):
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date

    def __repr__(self):
        return f"Enrollment(student_id={self.student_id}, course_id={self.course_id}, enrollment_date={self.enrollment_date})"