from PyQt6.QtWidgets import QMessageBox
from src.bll.enrollment_bll import EnrollmentBLL

class EnrollmentController:
    def __init__(self):
        self.enrollment_bll = EnrollmentBLL()

    def enroll_student(self, student_id, course_id):
        success = self.enrollment_bll.enroll_student(student_id, course_id)
        if success:
            QMessageBox.information(None, "Success", "Student enrolled successfully.")
        else:
            QMessageBox.warning(None, "Error", "Enrollment failed. Please try again.")

    def get_enrollment_details(self, enrollment_id):
        return self.enrollment_bll.get_enrollment_details(enrollment_id)

    def remove_enrollment(self, enrollment_id):
        success = self.enrollment_bll.remove_enrollment(enrollment_id)
        if success:
            QMessageBox.information(None, "Success", "Enrollment removed successfully.")
        else:
            QMessageBox.warning(None, "Error", "Failed to remove enrollment. Please try again.")