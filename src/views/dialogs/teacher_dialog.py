from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class TeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Teacher Dialog")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.label_name = QLabel("Name:")
        self.input_name = QLineEdit()
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.input_name)

        self.label_subject = QLabel("Subject:")
        self.input_subject = QLineEdit()
        self.layout.addWidget(self.label_subject)
        self.layout.addWidget(self.input_subject)

        self.button_save = QPushButton("Save")
        self.layout.addWidget(self.button_save)

        self.setLayout(self.layout)

        self.button_save.clicked.connect(self.save_teacher)

    def save_teacher(self):
        name = self.input_name.text()
        subject = self.input_subject.text()
        # Logic to save teacher information goes here
        print(f"Teacher saved: {name}, Subject: {subject}")
        self.accept()