from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class StudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Student Dialog")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.label_name = QLabel("Name:")
        self.input_name = QLineEdit()
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.input_name)

        self.label_age = QLabel("Age:")
        self.input_age = QLineEdit()
        self.layout.addWidget(self.label_age)
        self.layout.addWidget(self.input_age)

        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_student)
        self.layout.addWidget(self.button_save)

        self.setLayout(self.layout)

    def save_student(self):
        name = self.input_name.text()
        age = self.input_age.text()
        # Logic to save the student data would go here
        print(f"Student saved: Name={name}, Age={age}")
        self.accept()