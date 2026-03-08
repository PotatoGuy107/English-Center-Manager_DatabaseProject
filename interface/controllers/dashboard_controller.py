from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSignal

from interface.views.generated.dashboard_ui import Ui_MainWindow
from infrastructure.repositories.dashboard_repository import DashboardRepository


class DashboardController(QMainWindow):
    go_to_teacher = pyqtSignal()
    go_to_course = pyqtSignal()
    go_to_room = pyqtSignal()
    go_to_user = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_quanlygiangvien.clicked.connect(self.go_to_teacher.emit)
        self.ui.pushButton_quanlykhoahoc.clicked.connect(self.go_to_course.emit)
        self.ui.pushButton_quanlyphonghoc.clicked.connect(self.go_to_room.emit)
        self.ui.pushButton_quanlytaikhoan.clicked.connect(self.go_to_user.emit)

        if hasattr(self.ui, "pushButton_dangxuat"):
            self.ui.pushButton_dangxuat.clicked.connect(self.handle_logout)

        self.update_stats()

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def update_stats(self):
        try:
            if hasattr(self.ui, "label_sophong"):
                self.ui.label_sophong.setText(str(DashboardRepository.get_room_count()))
            if hasattr(self.ui, "label_sohocvien"):
                self.ui.label_sohocvien.setText(str(DashboardRepository.get_student_count()))
            if hasattr(self.ui, "label_sokhoahoc"):
                self.ui.label_sokhoahoc.setText(str(DashboardRepository.get_course_count()))
            if hasattr(self.ui, "label_sogiangvien"):
                self.ui.label_sogiangvien.setText(str(DashboardRepository.get_teacher_count()))
        except Exception as e:
            print(f"Dashboard stats error: {e}")
