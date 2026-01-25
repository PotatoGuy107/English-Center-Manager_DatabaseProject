from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem

class TeacherView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Management")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Manage Teachers")
        self.layout.addWidget(self.label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Subject"])
        self.layout.addWidget(self.table)
        
        self.add_button = QPushButton("Add Teacher")
        self.layout.addWidget(self.add_button)
        
        self.setLayout(self.layout)