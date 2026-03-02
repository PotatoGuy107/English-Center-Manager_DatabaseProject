from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox,
    QVBoxLayout, QTableWidgetItem, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from gdien.manhinhquanlyuser import Ui_MainWindow
from MODELS.user_model import UserModel


class QlyUserController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()  # Thêm tín hiệu đăng xuất để quay về màn hình Login

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối quay lại màn hình tổng
        self.ui.pushButton_quaylai3.clicked.connect(self.go_back.emit)

        # Xử lý Đăng xuất
        if hasattr(self.ui, 'pushButton_dangxuat4'):
            self.ui.pushButton_dangxuat4.clicked.connect(self.hanh_dong_dang_xuat)

        self.ui.pushButton_them3.clicked.connect(self.hanh_dong_them_user)
        self.ui.pushButton_sua2.clicked.connect(self.hanh_dong_sua_user)
        self.ui.pushButton_xoa2.clicked.connect(self.hanh_dong_xoa_user)

        self.load_data_user()

    def hanh_dong_dang_xuat(self):
        """Xác nhận và yêu cầu hệ thống chuyển về màn hình Login"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Phát tín hiệu báo cho file main.py biết để đổi màn hình
            self.logout_requested.emit()
            # Lưu ý: Không dùng self.close() ở đây vì nó sẽ tắt luôn cả app.
            # File main.py sẽ lo việc ẩn màn hình này đi.

    def load_data_user(self):
        data = UserModel.get_all_students()
        self.ui.table_quanly4.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa chuyên nghiệp
                self.ui.table_quanly4.setItem(row_idx, col_idx, item)

    def mo_form_nhap_lieu(self, tieu_de, data=None):
        """SỬA STYLE: Đồng bộ màu đỏ đô (#bc1823) và hồng nhạt (#ffecee)"""
        dialog = QDialog(self)
        dialog.setWindowTitle(tieu_de)

        # Thiết kế style đồng nhất với các màn hình khác của nhóm
        dialog.setStyleSheet("""
            QDialog { background-color: white; border: 2px solid #bc1823; }
            QLabel { color: #bc1823; font-weight: bold; }
            QLineEdit { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QPushButton { background-color: #bc1823; color: white; font-weight: bold; min-width: 80px; padding: 5px; }
        """)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()

        self.inputs = {
            'id': QLineEdit(),
            'name': QLineEdit(),
            'phone': QLineEdit(),
            'email': QLineEdit(),
            'status': QLineEdit()
        }

        if data:
            self.inputs['id'].setText(str(data[0]))
            self.inputs['id'].setReadOnly(True)
            self.inputs['name'].setText(str(data[1]))
            self.inputs['phone'].setText(str(data[2]))
            self.inputs['email'].setText(str(data[3]))
            self.inputs['status'].setText(str(data[4]))

        form_layout.addRow("Mã Học viên:", self.inputs['id'])
        form_layout.addRow("Họ và Tên:", self.inputs['name'])
        form_layout.addRow("SĐT:", self.inputs['phone'])
        form_layout.addRow("Email:", self.inputs['email'])
        form_layout.addRow("Trạng thái:", self.inputs['status'])

        layout.addLayout(form_layout)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return [i.text() for i in self.inputs.values()]

        return None

    def hanh_dong_them_user(self):
        res = self.mo_form_nhap_lieu("Thêm Học Viên Mới")
        if res:
            try:
                UserModel.insert_student(res)
                self.load_data_user()
                QMessageBox.information(self, "Thành công", "Đã thêm học viên mới!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def hanh_dong_sua_user(self):
        row = self.ui.table_quanly4.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên trước!")
            return

        old_data = [self.ui.table_quanly4.item(row, i).text() for i in range(5)]
        res = self.mo_form_nhap_lieu("Chỉnh sửa Học Viên", old_data)
        if res:
            try:
                UserModel.update_student(res)
                self.load_data_user()
                QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin học viên!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def hanh_dong_xoa_user(self):
        row = self.ui.table_quanly4.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên trước!")
            return

        student_id = self.ui.table_quanly4.item(row, 0).text()
        reply = QMessageBox.question(
            self, "Xác nhận", f"Bạn có chắc muốn xóa học viên {student_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                UserModel.delete_student(student_id)
                self.load_data_user()  # Tự động refresh bảng
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))