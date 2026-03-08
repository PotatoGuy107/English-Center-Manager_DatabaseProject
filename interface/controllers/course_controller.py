from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QDialog,
    QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox,
)
from PyQt6.QtCore import pyqtSignal, QEvent, Qt

from interface.views.generated.course_ui import Ui_MainWindow
from infrastructure.repositories.course_repository import CourseRepository


class CourseController(QMainWindow):
    go_back = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_quaylai.clicked.connect(self.go_back.emit)

        if hasattr(self.ui, "pushButton_dangxuat"):
            self.ui.pushButton_dangxuat.clicked.connect(self.handle_logout)

        self.ui.pushButton_them.clicked.connect(self.handle_add)
        self.ui.pushButton_sua.clicked.connect(self.handle_update)
        self.ui.pushButton_xoa.clicked.connect(self.handle_delete)

        self._skill_buttons = [
            self.ui.pushButton_c01,
            self.ui.pushButton_c02,
            self.ui.pushButton_c03,
            self.ui.pushButton_c05,
        ]
        for btn in self._skill_buttons:
            btn.installEventFilter(self)

        self._hide_all_skill_buttons()
        self.load_courses()

    def _hide_all_skill_buttons(self):
        for btn in [
            self.ui.pushButton_listening,
            self.ui.pushButton_speaking,
            self.ui.pushButton_reading,
            self.ui.pushButton_writing,
        ]:
            if hasattr(self.ui, btn.objectName()):
                btn.hide()

    def eventFilter(self, source, event):
        if source in (self.ui.pushButton_c01, self.ui.pushButton_c02):
            if event.type() == QEvent.Type.Enter:
                self._hide_all_skill_buttons()
                self.ui.pushButton_listening.show()
                self.ui.pushButton_speaking.show()
            elif event.type() == QEvent.Type.Leave:
                self._hide_all_skill_buttons()
        elif source in (self.ui.pushButton_c03, self.ui.pushButton_c05):
            if event.type() == QEvent.Type.Enter:
                self._hide_all_skill_buttons()
                self.ui.pushButton_listening.show()
                self.ui.pushButton_speaking.show()
                self.ui.pushButton_reading.show()
                self.ui.pushButton_writing.show()
            elif event.type() == QEvent.Type.Leave:
                self._hide_all_skill_buttons()
        return super().eventFilter(source, event)

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

    def load_courses(self):
        rows = CourseRepository.get_all_courses()
        self.ui.table_quanly.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.table_quanly.setItem(row_idx, col_idx, item)

    def show_input_form(self, title, data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setStyleSheet("QDialog { background-color: white; border: 2px solid #bc1823; }")
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        self.inputs = {
            "id": QLineEdit(), "name": QLineEdit(),
            "fee": QLineEdit(), "time": QLineEdit(),
        }
        if data:
            self.inputs["id"].setText(data[0]); self.inputs["id"].setReadOnly(True)
            self.inputs["name"].setText(data[1])
            self.inputs["fee"].setText(data[2])
            self.inputs["time"].setText(data[3])
        for k, v in self.inputs.items():
            form_layout.addRow(f"{k}:", v)
        layout.addLayout(form_layout)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept); btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        return [i.text() for i in self.inputs.values()] if dialog.exec() == QDialog.DialogCode.Accepted else None

    def handle_add(self):
        res = self.show_input_form("Add Course")
        if res:
            CourseRepository.insert_course(res)
            self.load_courses()

    def handle_update(self):
        row = self.ui.table_quanly.currentRow()
        if row >= 0:
            old = [self.ui.table_quanly.item(row, i).text() for i in range(4)]
            res = self.show_input_form("Edit Course", old)
            if res:
                CourseRepository.update_course(res)
                self.load_courses()

    def handle_delete(self):
        row = self.ui.table_quanly.currentRow()
        if row >= 0:
            course_id = self.ui.table_quanly.item(row, 0).text()
            if QMessageBox.question(self, "Delete", f"Delete course {course_id}?") == QMessageBox.StandardButton.Yes:
                CourseRepository.delete_course(course_id)
                self.load_courses()
