from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSignal

from interface.views.generated.login_ui import Ui_MainWindow
from infrastructure.repositories.auth_repository import AuthRepository


class LoginController(QMainWindow):
    # Emit role and ref_id (teacher_id or staff_id)
    login_success = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = AuthRepository()
        self.ui.pushButton_dangnhap.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_1.text().strip()
        result = self.model.check_login(username, password)
        if result:
            ref_id = result.get("ref_id", "") or ""
            self.login_success.emit(result["role"], ref_id)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
