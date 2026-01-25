from PyQt6.QtWidgets import QMessageBox
from src.bll.course_bll import CourseBLL

class CourseController:
    def __init__(self):
        self.course_bll = CourseBLL()

    def add_course(self, course_data):
        try:
            self.course_bll.add_course(course_data)
            QMessageBox.information(None, "Success", "Course added successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to add course: {str(e)}")

    def update_course(self, course_id, course_data):
        try:
            self.course_bll.update_course(course_id, course_data)
            QMessageBox.information(None, "Success", "Course updated successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to update course: {str(e)}")

    def delete_course(self, course_id):
        try:
            self.course_bll.delete_course(course_id)
            QMessageBox.information(None, "Success", "Course deleted successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to delete course: {str(e)}")

    def get_all_courses(self):
        try:
            return self.course_bll.get_all_courses()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to retrieve courses: {str(e)}")
            return []