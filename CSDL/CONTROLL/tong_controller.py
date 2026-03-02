from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSignal
from gdien.manhinhtong import Ui_MainWindow
from MODELS.tong_model import DashboardModel


class ManHinhTongController(QMainWindow):
    go_to_giangvien = pyqtSignal()
    go_to_khoahoc = pyqtSignal()
    go_to_phonghoc = pyqtSignal()
    go_to_user = pyqtSignal()
    logout_requested = pyqtSignal()  # Thêm tín hiệu đăng xuất

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Chuyển trang
        self.ui.pushButton_quanlygiangvien.clicked.connect(self.go_to_giangvien.emit)
        self.ui.pushButton_quanlykhoahoc.clicked.connect(self.go_to_khoahoc.emit)
        self.ui.pushButton_quanlyphonghoc.clicked.connect(self.go_to_phonghoc.emit)
        self.ui.pushButton_quanlytaikhoan.clicked.connect(self.go_to_user.emit)

        # Cấu hình nút đăng xuất
        if hasattr(self.ui, 'pushButton_dangxuat'):
            self.ui.pushButton_dangxuat.clicked.connect(self.hanh_dong_dang_xuat)

        self.update_stats()

    def hanh_dong_dang_xuat(self):
        """Xác nhận và phát tín hiệu đăng xuất"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()  # Gửi tín hiệu về MainApp để chuyển trang

    def update_stats(self):
        try:
            ro = DashboardModel.get_room_count()
            st = DashboardModel.get_student_count()
            co = DashboardModel.get_course_count()
            te = DashboardModel.get_teacher_count()

            if hasattr(self.ui, 'label_sophong'):
                self.ui.label_sophong.setText(str(ro))

            if hasattr(self.ui, 'label_sohocvien'):
                self.ui.label_sohocvien.setText(str(st))

            if hasattr(self.ui, 'label_sokhoahoc'):
                self.ui.label_sokhoahoc.setText(str(co))

            if hasattr(self.ui, 'label_sogiangvien'):
                self.ui.label_sogiangvien.setText(str(te))

        except Exception as e:
            print(f"Lỗi Dashboard: {e}")