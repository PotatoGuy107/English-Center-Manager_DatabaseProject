from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt
from BILL.payment_bll import PaymentBLL
from gdien.manhinhthanhtoan import Ui_MainWindow


class ManHinhThanhToanController(QMainWindow):
    def __init__(self, class_code=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.parent_window = parent

        if self.class_code:
            self.setWindowTitle(f"Thanh toán học phí - Lớp {self.class_code}")

        self.ui.danhsachlopday.setRowCount(0)

        self.bll = PaymentBLL()
        self.connect_signals()

        if self.class_code:
            self.load_students()
            self.load_data()

    # ================= CONNECT =================
    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.go_back)
        self.ui.pushButton_luu.clicked.connect(self.save_data)
        self.ui.pushButton_xoa3_2.clicked.connect(self.clear_payment_data)

    

    # ================= LOAD HỌC VIÊN =================
    def load_students(self):
        students = self.bll.get_students_by_class(self.class_code)
        table = self.ui.danhsachlopday
        table.setRowCount(0)

        for row_index, s in enumerate(students):
            table.insertRow(row_index)

            # STT
            item_stt = QTableWidgetItem(str(row_index + 1))
            item_stt.setFlags(Qt.ItemFlag.ItemIsEnabled)
            table.setItem(row_index, 0, item_stt)

            # Mã HV
            item_id = QTableWidgetItem(s.student_id)
            item_id.setFlags(Qt.ItemFlag.ItemIsEnabled)
            table.setItem(row_index, 1, item_id)

            # Tên HV
            item_name = QTableWidgetItem(s.name)
            item_name.setFlags(Qt.ItemFlag.ItemIsEnabled)
            table.setItem(row_index, 2, item_name)

            # Các cột thanh toán
            for col in range(3, table.columnCount()):
                table.setItem(row_index, col, QTableWidgetItem(""))

    # ================= LOAD THANH TOÁN =================
    def load_data(self):
        payments = self.bll.get_payment(self.class_code)
        table = self.ui.danhsachlopday

        for row in range(table.rowCount()):
            student_id = table.item(row, 1).text()

            for p in payments:
                if p.student_id == student_id:
                    table.setItem(row, 3, QTableWidgetItem(p.payment_code))
                    table.setItem(row, 4, QTableWidgetItem(str(p.amount)))
                    table.setItem(row, 5, QTableWidgetItem(p.payment_date))
                    table.setItem(row, 6, QTableWidgetItem(p.status))
                    table.setItem(row, 7, QTableWidgetItem(p.note))

    # ================= LƯU =================
    def save_data(self):
        table = self.ui.danhsachlopday
        data = []

        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                row_data.append(item.text().strip() if item else "")
            data.append(row_data)

        self.bll.save_payment(self.class_code, data)

        QMessageBox.information(self, "Thành công", "Đã lưu dữ liệu")

    # ================= XOÁ DỮ LIỆU THANH TOÁN =================
    def clear_payment_data(self):
        table = self.ui.danhsachlopday
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Chưa chọn dòng", "Vui lòng chọn dòng")
            return

        for col in range(3, table.columnCount()):
            table.setItem(row, col, QTableWidgetItem(""))

    # ================= TRỞ VỀ =================
    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()