from PyQt6 import QtWidgets, uic

class CourseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('src/views/dialogs/course_dialog.ui', self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Course Management")
        self.save_button.clicked.connect(self.save_course)
        self.cancel_button.clicked.connect(self.reject)

    def save_course(self):
        course_name = self.course_name_input.text()
        course_description = self.course_description_input.toPlainText()
        # Here you would typically call the controller to save the course
        # For example: self.controller.save_course(course_name, course_description)
        print(f"Course saved: {course_name}, {course_description}")
        self.accept()