from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSignal
from gdien.manhinhdangnhap import Ui_MainWindow
from MODELS.dangnhap_model import LoginModel


class LoginController(QMainWindow):
    # Phát tín hiệu kèm theo chuỗi vai trò (str)
    login_success = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Khởi tạo model
        # Khi dòng này chạy, LoginModel sẽ tự động kiểm tra và tạo bảng Account nếu chưa có
        self.model = LoginModel()

        self.ui.pushButton_dangnhap.clicked.connect(self.handle_login)

    def handle_login(self):
        """Xử lý logic đăng nhập và phát tín hiệu điều hướng"""
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_1.text()

        # Gọi hàm kiểm tra từ model
        user_data = self.model.check_login(username, password)

        if user_data:
            role = user_data["role"]
            QMessageBox.information(self, "Thành công", f"Chào mừng {username} ({role})!")

            # Gửi vai trò sang file main1.py để điều hướng màn hình
            self.login_success.emit(role)
        else:
            QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")