from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from controllers.course_controller import CourseController

class CourseView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Management")
        self.layout = QVBoxLayout()

        self.label = QLabel("Course Management")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.add_button = QPushButton("Add Course")
        self.add_button.clicked.connect(self.add_course)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

        self.controller = CourseController()
        self.load_courses()

    def load_courses(self):
        courses = self.controller.get_all_courses()
        self.table.setRowCount(len(courses))
        self.table.setColumnCount(3)  # Assuming 3 columns: ID, Name, Credits
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Credits"])

        for row, course in enumerate(courses):
            self.table.setItem(row, 0, QTableWidgetItem(str(course.id)))
            self.table.setItem(row, 1, QTableWidgetItem(course.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(course.credits)))

    def add_course(self):
        # Logic to add a course (e.g., open a dialog to input course details)
        pass