from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtCore import pyqtSignal

from interface.views.generated.login_ui import Ui_MainWindow
from infrastructure.repositories.auth_repository import AuthRepository

# Common input styling for visibility
INPUT_STYLE = """
    QLineEdit {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QLineEdit:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
    QLineEdit::placeholder {
        color: #999;
    }
"""


class LoginController(QMainWindow):
    # Emit role and ref_id (teacher_id or staff_id)
    login_success = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = AuthRepository()
        
        # Apply input styling
        self.ui.lineEdit.setStyleSheet(INPUT_STYLE)
        self.ui.lineEdit.setPlaceholderText("Tên đăng nhập")
        self.ui.lineEdit_1.setStyleSheet(INPUT_STYLE)
        self.ui.lineEdit_1.setPlaceholderText("Mật khẩu")
        # Hide password with dots/asterisks
        self.ui.lineEdit_1.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.ui.pushButton_dangnhap.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_1.text().strip()
        result = self.model.check_login(username, password)
        if result:
            ref_id = result.get("ref_id", "") or ""
            self.login_success.emit(result["role"], str(ref_id))
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
