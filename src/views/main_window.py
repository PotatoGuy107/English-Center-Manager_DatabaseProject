from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("English Center Manager")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Welcome to the English Center Manager")
        layout.addWidget(label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)