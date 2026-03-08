from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox,
    QVBoxLayout, QTableWidgetItem,
)
from PyQt6.QtCore import pyqtSignal, Qt
from datetime import date

from interface.views.generated.teacher_ui import Ui_MainWindow
from infrastructure.repositories.teacher_repository import TeacherRepository


class TeacherController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_quaylai1.clicked.connect(self.go_back.emit)

        if hasattr(self.ui, "pushButton_dangxuat1"):
            self.ui.pushButton_dangxuat1.clicked.connect(self.handle_logout)

        self.ui.pushButton_them2.clicked.connect(self.handle_add)
        self.ui.pushButton_sua1.clicked.connect(self.handle_update)
        self.ui.pushButton_xoa1.clicked.connect(self.handle_delete)

        self.load_data()

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def load_data(self):
        rows = TeacherRepository.get_all()
        self.ui.table_quanly1.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.table_quanly1.setItem(row_idx, col_idx, item)

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
        form = QFormLayout()
        # Schema: teacher_id, full_name, phone_number, email, specialization, hire_date, status
        labels = ["ID:", "Full Name:", "Phone:", "Email:", "Specialization:", "Hire Date:", "Status:"]
        self.inputs = [QLineEdit() for _ in range(7)]
        if data:
            for i in range(min(len(data), 7)):
                self.inputs[i].setText(str(data[i]) if data[i] else "")
            self.inputs[0].setReadOnly(True)
        else:
            # Adding new teacher - ID is auto-generated
            self.inputs[0].setText("(Auto)")
            self.inputs[0].setReadOnly(True)
        for i in range(7):
            form.addRow(labels[i], self.inputs[i])
        layout.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return [i.text() for i in self.inputs]
        return None

    def handle_add(self):
        data = self.show_input_form("Add Teacher")
        if data:
            try:
                # data = (full_name, phone, email, specialization, hire_date, status) - teacher_id is auto-generated
                hire_date = data[5] if data[5] else date.today().strftime("%Y-%m-%d")
                teacher_data = (data[1], data[2], data[3], data[4], hire_date, data[6] or "Active")
                new_id = TeacherRepository.insert(teacher_data)
                self.load_data()
                QMessageBox.information(self, "Success", f"Teacher {new_id} added successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def handle_update(self):
        row = self.ui.table_quanly1.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a teacher first!")
            return
        # Get 7 columns from table
        col_count = self.ui.table_quanly1.columnCount()
        old_data = [self.ui.table_quanly1.item(row, i).text() if self.ui.table_quanly1.item(row, i) else "" for i in range(col_count)]
        data = self.show_input_form("Edit Teacher", old_data)
        if data:
            try:
                # data = (teacher_id, full_name, phone, email, specialization, hire_date, status)
                TeacherRepository.update(tuple(data))
                self.load_data()
                QMessageBox.information(self, "Success", "Teacher updated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def handle_delete(self):
        row = self.ui.table_quanly1.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a teacher first!")
            return
        teacher_id = self.ui.table_quanly1.item(row, 0).text()
        reply = QMessageBox.question(
            self, "Confirm", f"Delete teacher {teacher_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                TeacherRepository.delete(teacher_id)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
