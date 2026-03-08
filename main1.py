import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

# ===== FIX ROOT PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ===== IMPORT CONTROLLER =====
from CONTROLL.dangnhap_controller import LoginController
from CONTROLL.tong_controller import ManHinhTongController
from CONTROLL.khoahoc_controller import QlyKhoaHocController
from CONTROLL.giangvien_controller import QlyGiangVienController
from CONTROLL.phonghoc_controller import QlyPhongHocController
from CONTROLL.user_controller import QlyUserController

# Link thêm 2 Controller từ các file main khác
from CONTROLL.controllclass import TaoLopController
from CONTROLL.teacher.classlist_controll import TeacherClassList


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hệ thống Quản lý Trung tâm Anh ngữ")
        self.setFixedSize(945, 600)

        # STACK SCREEN
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # ===== CREATE SCREEN =====
        self.login = LoginController()
        self.home = ManHinhTongController()
        self.khoahoc = QlyKhoaHocController()
        self.giangvien = QlyGiangVienController()
        self.phonghoc = QlyPhongHocController()
        self.user = QlyUserController()

        # Khởi tạo thêm 2 màn hình từ main.py và main_teacher.py
        self.taolop_staff = TaoLopController()
        self.teacher_view = TeacherClassList()

        # ===== ADD STACK =====
        self.stack.addWidget(self.login)  # Index 0
        self.stack.addWidget(self.home)  # Index 1
        self.stack.addWidget(self.khoahoc)  # Index 2
        self.stack.addWidget(self.giangvien)  # Index 3
        self.stack.addWidget(self.phonghoc)  # Index 4
        self.stack.addWidget(self.user)  # Index 5
        self.stack.addWidget(self.taolop_staff)  # Index 6
        self.stack.addWidget(self.teacher_view)  # Index 7

        self.connect_signal()

        # Khởi động ứng dụng tại màn hình Đăng nhập
        self.stack.setCurrentWidget(self.login)

    # ===============================
    # SIGNAL NAVIGATION
    # ===============================
    def connect_signal(self):
        # 1. Xử lý Đăng nhập thành công -> Phân quyền điều hướng
        self.login.login_success.connect(self.dieu_huong_theo_vai_tro)

        # 2. Điều hướng từ màn hình Tổng đi các trang quản lý
        self.home.go_to_khoahoc.connect(lambda: self.stack.setCurrentWidget(self.khoahoc))
        self.home.go_to_giangvien.connect(lambda: self.stack.setCurrentWidget(self.giangvien))
        self.home.go_to_phonghoc.connect(lambda: self.stack.setCurrentWidget(self.phonghoc))
        self.home.go_to_user.connect(lambda: self.stack.setCurrentWidget(self.user))

        # Link nút chuyển sang màn hình Tạo Lớp nếu Trầm có nút này trên Dashboard
        if hasattr(self.home, "go_to_taolop"):
            self.home.go_to_taolop.connect(lambda: self.stack.setCurrentWidget(self.taolop_staff))

        # 3. Quay lại màn hình Tổng từ các trang con
        self.khoahoc.go_back.connect(self.back_home)
        self.giangvien.go_back.connect(self.back_home)
        self.phonghoc.go_back.connect(self.back_home)
        self.user.go_back.connect(self.back_home)

        # Quay lại từ màn hình Tạo Lớp (file main.py cũ)
        if hasattr(self.taolop_staff, "go_back"):
            self.taolop_staff.go_back.connect(self.back_home)

        # 4. Xử lý Đăng xuất (Logout) quay về màn hình Đăng nhập
        controllers = [self.home, self.giangvien, self.user, self.phonghoc, self.khoahoc, self.taolop_staff,
                       self.teacher_view]
        for ctrl in controllers:
            if hasattr(ctrl, "logout_requested"):
                ctrl.logout_requested.connect(self.show_login)

    # ===============================
    # HÀM PHÂN QUYỀN (ĐÃ CHỈNH SỬA CHO STAFF)
    # ===============================
    def dieu_huong_theo_vai_tro(self, role):
        """Link đúng giao diện theo yêu cầu: Staff vào file main.py cũ"""
        if role == "admin":
            # Admin vào Dashboard chính
            self.back_home()
        elif role == "staff":
            # CHỖ CẦN CHỈNH: Staff vào thẳng màn hình Tạo lớp (file main.py)
            self.stack.setCurrentWidget(self.taolop_staff)
        elif role == "giangvien":
            # Giảng viên vào màn hình danh sách lớp (file main_teacher.py)
            self.stack.setCurrentWidget(self.teacher_view)

    # ===============================
    def back_home(self):
        """Cập nhật thống kê và hiển thị màn hình chính"""
        if hasattr(self.home, "update_stats"):
            self.home.update_stats()
        self.stack.setCurrentWidget(self.home)

    def show_login(self):
        """Quay về màn hình đăng nhập"""
        self.stack.setCurrentWidget(self.login)


# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())