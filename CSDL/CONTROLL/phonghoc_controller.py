from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from gdien.manhinhquanlyphonghoc import Ui_MainWindow
from MODELS.phonghoc_model import PhongHocModel


class QlyPhongHocController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()  # Tín hiệu kết nối về màn hình Login

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối quay lại màn hình tổng
        self.ui.pushButton_quaylai2.clicked.connect(self.go_back.emit)

        # Xử lý Đăng xuất tương tự file Tổng
        if hasattr(self.ui, 'pushButton_dangxuat2'):
            self.ui.pushButton_dangxuat2.clicked.connect(self.hanh_dong_dang_xuat)

        self.ui.pushButton_them2.clicked.connect(self.hanh_dong_them_phong)
        self.ui.pushButton_capnhat.clicked.connect(self.hanh_dong_cap_nhat)
        self.ui.pushButton_dongmo.clicked.connect(self.hanh_dong_dong_mo_phong)

        self.load_data_phong_hoc()

    def hanh_dong_dang_xuat(self):
        """Xác nhận đăng xuất đồng bộ style đỏ đô"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # Phát tín hiệu để MainApp thực hiện chuyển về màn hình Login
            self.logout_requested.emit()

    def load_data_phong_hoc(self):
        data = PhongHocModel.get_all_rooms()
        self.ui.table_quanly2.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # Căn giữa chuyên nghiệp
                self.ui.table_quanly2.setItem(row_idx, col_idx, item)

        if hasattr(self.ui, 'label_sophong'):
            self.ui.label_sophong.setText(str(len(data)))

    def mo_form_nhap_lieu(self, tieu_de, data=None):
        """SỬA STYLE: Đồng bộ màu đỏ đô và hồng nhạt"""
        dialog = QDialog(self)
        dialog.setWindowTitle(tieu_de)

        # Thiết kế style đỏ đô đặc trưng
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
            'cap': QLineEdit(),
            'type': QLineEdit(),
            'status': QLineEdit()
        }

        if data:
            self.inputs['id'].setText(str(data[0]))
            self.inputs['id'].setReadOnly(True)
            self.inputs['name'].setText(str(data[1]))
            self.inputs['cap'].setText(str(data[2]))
            self.inputs['type'].setText(str(data[3]))
            self.inputs['status'].setText(str(data[4]))

        form_layout.addRow("Mã Phòng:", self.inputs['id'])
        form_layout.addRow("Tên Phòng:", self.inputs['name'])
        form_layout.addRow("Sức chứa:", self.inputs['cap'])
        form_layout.addRow("Loại phòng:", self.inputs['type'])
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

    def hanh_dong_them_phong(self):
        res = self.mo_form_nhap_lieu("Thêm Phòng Học Mới")
        if res:
            try:
                PhongHocModel.insert_room(res)
                self.load_data_phong_hoc()
                QMessageBox.information(self, "Thành công", "Đã thêm phòng học mới!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def hanh_dong_cap_nhat(self):
        """Làm mới dữ liệu từ Database"""
        self.load_data_phong_hoc()
        QMessageBox.information(self, "Thông báo", "Đã cập nhật danh sách phòng!")

    def hanh_dong_dong_mo_phong(self):
        """Thay đổi trạng thái Active/Inactive"""
        row = self.ui.table_quanly2.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một dòng để đổi trạng thái!")
            return

        id_phong = self.ui.table_quanly2.item(row, 0).text()
        current_status = self.ui.table_quanly2.item(row, 4).text()

        # Đổi trạng thái linh hoạt
        new_status = "Inactive" if current_status == "Active" else "Active"

        try:
            PhongHocModel.update_status(id_phong, new_status)
            self.load_data_phong_hoc()
            QMessageBox.information(self, "Thành công", f"Phòng {id_phong} đã chuyển sang {new_status}!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))