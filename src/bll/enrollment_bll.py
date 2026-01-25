class EnrollmentBLL:
    def __init__(self, enrollment_dal):
        self.enrollment_dal = enrollment_dal

    def enroll_student(self, student_id, course_id):
        if self.enrollment_dal.is_student_enrolled(student_id, course_id):
            return "Student is already enrolled in this course."
        else:
            self.enrollment_dal.enroll_student(student_id, course_id)
            return "Student enrolled successfully."

    def withdraw_student(self, student_id, course_id):
        if not self.enrollment_dal.is_student_enrolled(student_id, course_id):
            return "Student is not enrolled in this course."
        else:
            self.enrollment_dal.withdraw_student(student_id, course_id)
            return "Student withdrawn successfully."

    def get_enrollment_list(self, course_id):
        return self.enrollment_dal.get_enrollment_list(course_id)