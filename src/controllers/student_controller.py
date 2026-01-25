from PyQt6.QtWidgets import QMessageBox
from src.models.student import Student
from src.bll.student_bll import StudentBLL

class StudentController:
    def __init__(self):
        self.student_bll = StudentBLL()

    def add_student(self, student_data):
        student = Student(**student_data)
        success = self.student_bll.add_student(student)
        if success:
            QMessageBox.information(None, "Success", "Student added successfully.")
        else:
            QMessageBox.warning(None, "Error", "Failed to add student.")

    def update_student(self, student_id, student_data):
        student = Student(id=student_id, **student_data)
        success = self.student_bll.update_student(student)
        if success:
            QMessageBox.information(None, "Success", "Student updated successfully.")
        else:
            QMessageBox.warning(None, "Error", "Failed to update student.")

    def delete_student(self, student_id):
        success = self.student_bll.delete_student(student_id)
        if success:
            QMessageBox.information(None, "Success", "Student deleted successfully.")
        else:
            QMessageBox.warning(None, "Error", "Failed to delete student.")

    def get_all_students(self):
        return self.student_bll.get_all_students()