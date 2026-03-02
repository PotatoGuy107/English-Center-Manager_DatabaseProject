from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox,
    QVBoxLayout, QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal, Qt
from gdien.manhinhquanlygiangvien import Ui_MainWindow
from MODELS.giangvien_model import GiangVienModel


class QlyGiangVienController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()  # Tín hiệu để quay về màn hình Login

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối quay lại màn hình tổng
        self.ui.pushButton_quaylai1.clicked.connect(self.go_back.emit)

        # Xử lý Đăng xuất chuẩn theo file User
        if hasattr(self.ui, 'pushButton_dangxuat1'):
            self.ui.pushButton_dangxuat1.clicked.connect(self.hanh_dong_dang_xuat)

        self.ui.pushButton_them2.clicked.connect(self.hanh_dong_them_gv)
        self.ui.pushButton_sua1.clicked.connect(self.hanh_dong_sua_gv)
        self.ui.pushButton_xoa1.clicked.connect(self.hanh_dong_xoa_gv)

        self.load_data()

    def hanh_dong_dang_xuat(self):
        """Xử lý xác nhận và phát tín hiệu đăng xuất chuẩn nhất"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Phát tín hiệu báo cho file main.py biết để đổi màn hình
            self.logout_requested.emit()

    def load_data(self):
        """Tải dữ liệu và căn giữa các ô y hệt file User"""
        rows = GiangVienModel.get_all()
        self.ui.table_quanly1.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa chuyên nghiệp
                self.ui.table_quanly1.setItem(row_idx, col_idx, item)

    def mo_form_nhap_lieu(self, title, data=None):
        """Form nhập liệu đồng bộ màu đỏ đô và hồng nhạt"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setStyleSheet("""
            QDialog { background-color: white; border: 2px solid #bc1823; }
            QLabel { color: #bc1823; font-weight: bold; }
            QLineEdit { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QPushButton { background-color: #bc1823; color: white; font-weight: bold; min-width: 80px; padding: 5px; }
        """)

        layout = QVBoxLayout(dialog)
        form = QFormLayout()

        labels = ["Mã GV:", "Họ và Tên:", "Chuyên môn:", "Bằng cấp:", "SĐT:", "Trạng thái:"]
        self.inputs = [QLineEdit() for _ in range(6)]

        if data:
            for i in range(6):
                self.inputs[i].setText(str(data[i]))
            self.inputs[0].setReadOnly(True)

        for i in range(6):
            form.addRow(labels[i], self.inputs[i])

        layout.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return [i.text() for i in self.inputs]
        return None

    def hanh_dong_them_gv(self):
        data = self.mo_form_nhap_lieu("Thêm Giảng Viên Mới")
        if data:
            try:
                GiangVienModel.insert(data)
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã thêm giảng viên mới!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def hanh_dong_sua_gv(self):
        row = self.ui.table_quanly1.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn giảng viên trước!")
            return

        old_data = [self.ui.table_quanly1.item(row, i).text() for i in range(6)]
        data = self.mo_form_nhap_lieu("Chỉnh sửa Giảng viên", old_data)
        if data:
            try:
                GiangVienModel.update(data)
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def hanh_dong_xoa_gv(self):
        row = self.ui.table_quanly1.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn giảng viên trước!")
            return

        id_gv = self.ui.table_quanly1.item(row, 0).text()
        reply = QMessageBox.question(
            self, "Xác nhận", f"Bạn có chắc muốn xóa giảng viên {id_gv}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                GiangVienModel.delete(id_gv)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))