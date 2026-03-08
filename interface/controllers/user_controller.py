from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox,
    QVBoxLayout, QTableWidgetItem,
)
from PyQt6.QtCore import pyqtSignal, Qt

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
        self.ui.table_quanly4.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.table_quanly4.setItem(row_idx, col_idx, item)

    def show_input_form(self, title, data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setStyleSheet("""
            QDialog { background-color: white; border: 2px solid #bc1823; }
            QLabel { color: #bc1823; font-weight: bold; }
            QLineEdit { background-color: #ffecee; border: 1px solid #bc1823; padding: 5px; color: black; }
            QPushButton { background-color: #bc1823; color: white; font-weight: bold; min-width: 80px; padding: 5px; }
        """)
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        self.inputs = {
            "id": QLineEdit(), "name": QLineEdit(),
            "phone": QLineEdit(), "email": QLineEdit(), "status": QLineEdit(),
        }
        if data:
            keys = list(self.inputs.keys())
            for i, key in enumerate(keys):
                self.inputs[key].setText(str(data[i]))
            self.inputs["id"].setReadOnly(True)
        labels = ["Student ID:", "Full Name:", "Phone:", "Email:", "Status:"]
        for label, key in zip(labels, self.inputs):
            form_layout.addRow(label, self.inputs[key])
        layout.addLayout(form_layout)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return [i.text() for i in self.inputs.values()]
        return None

    def handle_add(self):
        res = self.show_input_form("Add Student")
        if res:
            try:
                StudentDbRepository.insert_student(res)
                self.load_data()
                QMessageBox.information(self, "Success", "Student added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def handle_update(self):
        row = self.ui.table_quanly4.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a student first!")
            return
        old_data = [self.ui.table_quanly4.item(row, i).text() for i in range(5)]
        res = self.show_input_form("Edit Student", old_data)
        if res:
            try:
                StudentDbRepository.update_student(res)
                self.load_data()
                QMessageBox.information(self, "Success", "Student updated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def handle_delete(self):
        row = self.ui.table_quanly4.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a student first!")
            return
        student_id = self.ui.table_quanly4.item(row, 0).text()
        reply = QMessageBox.question(
            self, "Confirm", f"Delete student {student_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                StudentDbRepository.delete_student(student_id)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
