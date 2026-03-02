from PyQt6.QtWidgets import (QMainWindow, QMessageBox, QTableWidgetItem, QDialog,
                             QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox)
from PyQt6.QtCore import pyqtSignal, QEvent, Qt
from gdien.manhinhquanlykhoahoc import Ui_MainWindow
from MODELS.khoahoc_model import KhoaHocModel


class QlyKhoaHocController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ===== BUTTON =====
        self.ui.pushButton_quaylai.clicked.connect(self.go_back.emit)

        if hasattr(self.ui, 'pushButton_dangxuat'):
            self.ui.pushButton_dangxuat.clicked.connect(self.hanh_dong_dang_xuat)

        self.ui.pushButton_them.clicked.connect(self.hanh_dong_them)
        self.ui.pushButton_sua.clicked.connect(self.hanh_dong_sua)
        self.ui.pushButton_xoa.clicked.connect(self.hanh_dong_xoa)

        # ===== ĐĂNG KÝ SỰ KIỆN HOVER CHO CÁC KHUNG ĐÀO TẠO =====
        self.nut_dao_tao = [
            self.ui.pushButton_c01,  # Khung English Communication
            self.ui.pushButton_c02,  # Khung English Starter
            self.ui.pushButton_c03,  # Khung Cambridge
            self.ui.pushButton_c05  # Khung IELTS
        ]

        for nut in self.nut_dao_tao:
            if hasattr(self.ui, nut.objectName()):
                nut.installEventFilter(self)  # Cài đặt bộ lọc sự kiện

        # Ẩn các nút kỹ năng lúc mới vào
        self.an_tat_ca_nut_ky_nang()

        self.load_data_khoa_hoc()

    def an_tat_ca_nut_ky_nang(self):
        """Ẩn 4 pushButton kỹ năng bên phải"""
        nut_list = [
            self.ui.pushButton_listening,
            self.ui.pushButton_speaking,
            self.ui.pushButton_reading,
            self.ui.pushButton_writing
        ]
        for nut in nut_list:
            if hasattr(self.ui, nut.objectName()):
                nut.hide()

    def eventFilter(self, source, event):
        """Xử lý ẩn/hiện kỹ năng khi trỏ chuột vào khung trắng"""
        # Nhóm C01 và C02: Chỉ hiện Listening và Speaking
        if source == self.ui.pushButton_c01 or source == self.ui.pushButton_c02:
            if event.type() == QEvent.Type.Enter:
                self.an_tat_ca_nut_ky_nang()
                self.ui.pushButton_listening.show()
                self.ui.pushButton_speaking.show()
            elif event.type() == QEvent.Type.Leave:
                self.an_tat_ca_nut_ky_nang()

        # Nhóm C03 và C05: Hiện tất cả 4 kỹ năng
        elif source == self.ui.pushButton_c03 or source == self.ui.pushButton_c05:
            if event.type() == QEvent.Type.Enter:
                self.an_tat_ca_nut_ky_nang()
                self.ui.pushButton_listening.show()
                self.ui.pushButton_speaking.show()
                self.ui.pushButton_reading.show()
                self.ui.pushButton_writing.show()
            elif event.type() == QEvent.Type.Leave:
                self.an_tat_ca_nut_ky_nang()

        return super().eventFilter(source, event)

    # ===============================
    # CÁC CHỨC NĂNG KHÁC GIỮ NGUYÊN
    # ===============================
    def hanh_dong_dang_xuat(self):
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn đăng xuất?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def load_data_khoa_hoc(self):
        rows = KhoaHocModel.get_all_courses()
        self.ui.table_quanly.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.table_quanly.setItem(row_idx, col_idx, item)

    def mo_form_nhap_lieu(self, tieu_de, data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(tieu_de)
        dialog.setStyleSheet("QDialog { background-color: white; border: 2px solid #bc1823; }")
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        self.inputs = {'id': QLineEdit(), 'name': QLineEdit(), 'fee': QLineEdit(), 'time': QLineEdit()}
        if data:
            self.inputs['id'].setText(data[0]);
            self.inputs['id'].setReadOnly(True)
            self.inputs['name'].setText(data[1]);
            self.inputs['fee'].setText(data[2]);
            self.inputs['time'].setText(data[3])
        for k, v in self.inputs.items(): form_layout.addRow(f"{k}:", v)
        layout.addLayout(form_layout)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept);
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        return [i.text() for i in self.inputs.values()] if dialog.exec() == QDialog.DialogCode.Accepted else None

    def hanh_dong_them(self):
        res = self.mo_form_nhap_lieu("Thêm Khóa Học");
        KhoaHocModel.insert_course(res) if res else None;
        self.load_data_khoa_hoc()

    def hanh_dong_sua(self):
        row = self.ui.table_quanly.currentRow()
        if row >= 0:
            old = [self.ui.table_quanly.item(row, i).text() for i in range(4)]
            res = self.mo_form_nhap_lieu("Sửa Khóa Học", old);
            KhoaHocModel.update_course(res) if res else None;
            self.load_data_khoa_hoc()

    def hanh_dong_xoa(self):
        row = self.ui.table_quanly.currentRow()
        if row >= 0:
            id_kh = self.ui.table_quanly.item(row, 0).text()
            if QMessageBox.question(self, "Xóa", f"Xóa {id_kh}?") == QMessageBox.StandardButton.Yes:
                KhoaHocModel.delete_course(id_kh);
                self.load_data_khoa_hoc()