from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from controllers.student_controller import StudentController

class StudentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.layout = QVBoxLayout()

        self.student_name_label = QLabel("Student Name:")
        self.layout.addWidget(self.student_name_label)

        self.student_name_input = QLineEdit()
        self.layout.addWidget(self.student_name_input)

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        self.layout.addWidget(self.add_student_button)

        self.setLayout(self.layout)

        self.controller = StudentController()

    def add_student(self):
        student_name = self.student_name_input.text()
        if student_name:
            success = self.controller.add_student(student_name)
            if success:
                QMessageBox.information(self, "Success", "Student added successfully!")
                self.student_name_input.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to add student.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a student name.")