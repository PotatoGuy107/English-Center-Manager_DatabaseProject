from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox,
    QVBoxLayout, QTableWidgetItem, QComboBox, QDateEdit,
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtGui import QColor, QBrush

from interface.views.generated.user_ui import Ui_MainWindow
from infrastructure.repositories.student_db_repository import StudentDbRepository


class UserController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_quaylai3.clicked.connect(self.go_back.emit)

        if hasattr(self.ui, "pushButton_dangxuat4"):
            self.ui.pushButton_dangxuat4.clicked.connect(self.handle_logout)

        self.ui.pushButton_them3.clicked.connect(self.handle_add)
        self.ui.pushButton_sua2.clicked.connect(self.handle_update)
        self.ui.pushButton_xoa2.clicked.connect(self.handle_delete)

        self.load_data()

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def load_data(self):
        data = StudentDbRepository.get_all_students()
        
        # Setup table for 9 columns
        headers = ["ID", "Họ tên", "Ngày sinh", "Giới tính", "Địa chỉ", "SĐT", "Email", "Ngày ĐK", "Trạng thái"]
        self.ui.table_quanly4.setColumnCount(len(headers))
        self.ui.table_quanly4.setHorizontalHeaderLabels(headers)
        self.ui.table_quanly4.setRowCount(len(data))
        
        # Style the table for visibility
        self.ui.table_quanly4.setAlternatingRowColors(False)
        self.ui.table_quanly4.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #222;
                gridline-color: #ccc;
            }
            QTableWidget::item {
                color: #222;
                padding: 5px;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #bc1823;
                color: white;
            }
            QHeaderView::section {
                background-color: #bc1823;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #8b0000;
            }
        """)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                # Format dates for display
                if col_data is not None and hasattr(col_data, 'strftime'):
                    display_text = col_data.strftime("%d/%m/%Y")
                else:
                    display_text = str(col_data) if col_data is not None else ""
                item = QTableWidgetItem(display_text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QBrush(QColor("#222")))  # Dark text color
                self.ui.table_quanly4.setItem(row_idx, col_idx, item)

    def show_input_form(self, title, data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setStyleSheet("""
            QDialog { background-color: white; border: 2px solid #bc1823; }
            QLabel { color: #bc1823; font-weight: bold; }
            QLineEdit { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QDateEdit { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QComboBox { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QPushButton { background-color: #bc1823; color: white; font-weight: bold; min-width: 80px; padding: 5px; }
        """)
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Create input widgets for all 9 fields
        # DB order: student_id, full_name, date_of_birth, gender, address, phone_number, email, register_date, status
        self.input_id = QLineEdit()
        self.input_name = QLineEdit()
        self.input_dob = QDateEdit()
        self.input_dob.setCalendarPopup(True)
        self.input_dob.setDate(QDate(2000, 1, 1))
        self.input_gender = QComboBox()
        self.input_gender.addItems(["Nam", "Nữ", "Khác"])
        self.input_address = QLineEdit()
        self.input_phone = QLineEdit()
        self.input_email = QLineEdit()
        self.input_register_date = QDateEdit()
        self.input_register_date.setCalendarPopup(True)
        self.input_register_date.setDate(QDate.currentDate())
        self.input_status = QComboBox()
        self.input_status.addItems(["active", "inactive", "graduated"])
        
        self.inputs = {
            "id": self.input_id,
            "name": self.input_name,
            "dob": self.input_dob,
            "gender": self.input_gender,
            "address": self.input_address,
            "phone": self.input_phone,
            "email": self.input_email,
            "register_date": self.input_register_date,
            "status": self.input_status,
        }
        
        if data:
            # data: (student_id, full_name, date_of_birth, gender, address, phone_number, email, register_date, status)
            self.input_id.setText(str(data[0]))
            self.input_id.setReadOnly(True)
            self.input_name.setText(str(data[1]) if data[1] else "")
            if data[2]:  # date_of_birth
                self.input_dob.setDate(QDate(data[2].year, data[2].month, data[2].day))
            if data[3]:  # gender
                idx = self.input_gender.findText(str(data[3]))
                if idx >= 0:
                    self.input_gender.setCurrentIndex(idx)
            self.input_address.setText(str(data[4]) if data[4] else "")
            self.input_phone.setText(str(data[5]) if data[5] else "")
            self.input_email.setText(str(data[6]) if data[6] else "")
            if data[7]:  # register_date
                self.input_register_date.setDate(QDate(data[7].year, data[7].month, data[7].day))
            if data[8]:  # status
                idx = self.input_status.findText(str(data[8]))
                if idx >= 0:
                    self.input_status.setCurrentIndex(idx)
        else:
            # New student - hide ID field
            self.input_id.setVisible(False)
        
        labels_widgets = [
            ("Mã học viên:", self.input_id),
            ("Họ và tên:", self.input_name),
            ("Ngày sinh:", self.input_dob),
            ("Giới tính:", self.input_gender),
            ("Địa chỉ:", self.input_address),
            ("Số điện thoại:", self.input_phone),
            ("Email:", self.input_email),
            ("Ngày đăng ký:", self.input_register_date),
            ("Trạng thái:", self.input_status),
        ]
        for label, widget in labels_widgets:
            if data or label != "Mã học viên:":  # Hide ID label for new student
                form_layout.addRow(label, widget)
        
        layout.addLayout(form_layout)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Return tuple matching DB columns order (without student_id for insert, with for update)
            return {
                "id": self.input_id.text() if data else None,
                "name": self.input_name.text(),
                "dob": self.input_dob.date().toString("yyyy-MM-dd"),
                "gender": self.input_gender.currentText(),
                "address": self.input_address.text(),
                "phone": self.input_phone.text(),
                "email": self.input_email.text(),
                "register_date": self.input_register_date.date().toString("yyyy-MM-dd"),
                "status": self.input_status.currentText(),
            }
        return None

    def handle_add(self):
        res = self.show_input_form("Thêm học viên")
        if res:
            try:
                # res is dict: name, dob, gender, address, phone, email, register_date, status
                data = (
                    res["name"], res["dob"], res["gender"], res["address"],
                    res["phone"], res["email"], res["register_date"], res["status"]
                )
                new_id = StudentDbRepository.insert_student(data)
                self.load_data()
                QMessageBox.information(self, "Thành công", f"Đã thêm học viên (ID: {new_id})!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def handle_update(self):
        row = self.ui.table_quanly4.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên trước!")
            return
        # Get all 9 columns data from table
        students = StudentDbRepository.get_all_students()
        if row >= len(students):
            return
        old_data = students[row]
        res = self.show_input_form("Sửa học viên", old_data)
        if res:
            try:
                # res is dict with id, name, dob, gender, address, phone, email, register_date, status
                data = (
                    int(res["id"]),  # student_id
                    res["name"], res["dob"], res["gender"], res["address"],
                    res["phone"], res["email"], res["status"]
                )
                StudentDbRepository.update_student(data)
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã cập nhật học viên!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))

    def handle_delete(self):
        row = self.ui.table_quanly4.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên trước!")
            return
        student_id = self.ui.table_quanly4.item(row, 0).text()
        reply = QMessageBox.question(
            self, "Xác nhận", f"Xóa học viên ID {student_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                StudentDbRepository.delete_student(int(student_id))
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã xóa học viên!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", str(e))
