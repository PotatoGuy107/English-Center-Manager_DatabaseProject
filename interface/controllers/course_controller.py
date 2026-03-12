from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidgetItem, QDialog,
    QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox,
    QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox, QLabel, QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal, QEvent, Qt
from PyQt6.QtGui import QFont, QBrush, QColor

from interface.views.generated.course_ui import Ui_MainWindow
from infrastructure.repositories.course_repository import CourseRepository

# Course level options
COURSE_LEVELS = ["Beginner", "Elementary", "Intermediate", "Upper-Intermediate", "Advanced"]
# Course status options
COURSE_STATUS = ["Active", "Inactive", "Coming Soon"]


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
        # Thiết lập 7 cột: ID, KHOÁ HỌC, MÔ TẢ, CẤP ĐỘ, THỜI LƯỢNG, HỌC PHÍ, TRẠNG THÁI
        self.ui.table_quanly.setColumnCount(7)
        self.ui.table_quanly.setHorizontalHeaderLabels([
            "ID", "KHOÁ HỌC", "MÔ TẢ", "CẤP ĐỘ", "THỜI LƯỢNG", "HỌC PHÍ", "TRẠNG THÁI"
        ])
        self.ui.table_quanly.setAlternatingRowColors(False)
        self.ui.table_quanly.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
        self.ui.table_quanly.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QBrush(QColor("#222")))
                self.ui.table_quanly.setItem(row_idx, col_idx, item)
        # Điều chỉnh độ rộng cột
        self.ui.table_quanly.setColumnWidth(0, 50)   # ID
        self.ui.table_quanly.setColumnWidth(1, 150)  # KHOÁ HỌC
        self.ui.table_quanly.setColumnWidth(2, 200)  # MÔ TẢ
        self.ui.table_quanly.setColumnWidth(3, 120)  # CẤP ĐỘ
        self.ui.table_quanly.setColumnWidth(4, 90)   # THỜI LƯỢNG
        self.ui.table_quanly.setColumnWidth(5, 100)  # HỌC PHÍ
        self.ui.table_quanly.setColumnWidth(6, 100)  # TRẠNG THÁI

    def show_input_form(self, title, data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(450)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 2px solid #bc1823;
                border-radius: 10px;
            }
            QLabel {
                color: #bc1823;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #fff5f5;
                border: 2px solid #bc1823;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                color: #333;
                min-height: 20px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #8b0000;
                background-color: #ffe0e0;
            }
            QLineEdit:read-only {
                background-color: #e0e0e0;
                color: #666;
            }
            QPushButton {
                background-color: #bc1823;
                color: white;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
                min-height: 35px;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #8b0000;
            }
            QPushButton:pressed {
                background-color: #5c0000;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title label
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #bc1823; margin-bottom: 10px; min-width: auto;")
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # ID field (auto-generated)
        self.input_id = QLineEdit()
        self.input_id.setReadOnly(True)
        
        # Course name
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Enter course name...")
        
        # Description
        self.input_desc = QTextEdit()
        self.input_desc.setPlaceholderText("Enter course description...")
        self.input_desc.setMaximumHeight(80)
        
        # Level dropdown
        self.input_level = QComboBox()
        self.input_level.addItems(COURSE_LEVELS)
        
        # Duration (weeks)
        self.input_duration = QSpinBox()
        self.input_duration.setRange(1, 52)
        self.input_duration.setValue(12)
        self.input_duration.setSuffix(" weeks")
        
        # Tuition fee
        self.input_fee = QDoubleSpinBox()
        self.input_fee.setRange(0, 100000000)
        self.input_fee.setValue(5000000)
        self.input_fee.setSuffix(" VND")
        self.input_fee.setGroupSeparatorShown(True)
        
        # Status dropdown
        self.input_status = QComboBox()
        self.input_status.addItems(COURSE_STATUS)
        
        # Fill data if editing
        if data:
            self.input_id.setText(str(data[0]))
            self.input_name.setText(str(data[1]) if data[1] else "")
            self.input_desc.setText(str(data[2]) if data[2] else "")
            # Set level
            level_idx = self.input_level.findText(str(data[3])) if data[3] else 0
            self.input_level.setCurrentIndex(level_idx if level_idx >= 0 else 0)
            self.input_duration.setValue(int(data[4]) if data[4] else 12)
            self.input_fee.setValue(float(data[5]) if data[5] else 0)
            # Set status
            status_idx = self.input_status.findText(str(data[6])) if data[6] else 0
            self.input_status.setCurrentIndex(status_idx if status_idx >= 0 else 0)
        else:
            self.input_id.setText("(Auto)")
        
        # Add rows to form
        form_layout.addRow("Course ID:", self.input_id)
        form_layout.addRow("Course Name:", self.input_name)
        form_layout.addRow("Description:", self.input_desc)
        form_layout.addRow("Level:", self.input_level)
        form_layout.addRow("Duration:", self.input_duration)
        form_layout.addRow("Tuition Fee:", self.input_fee)
        form_layout.addRow("Status:", self.input_status)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btns)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return {
                "id": self.input_id.text(),
                "name": self.input_name.text(),
                "desc": self.input_desc.toPlainText(),
                "level": self.input_level.currentText(),
                "duration": self.input_duration.value(),
                "fee": self.input_fee.value(),
                "status": self.input_status.currentText(),
            }
        return None

    def handle_add(self):
        res = self.show_input_form("Add New Course")
        if res:
            try:
                # Schema: (course_name, description, level, duration_weeks, tuition_fee, status)
                course_data = (
                    res["name"],
                    res["desc"],
                    res["level"],
                    res["duration"],
                    res["fee"],
                    res["status"]
                )
                new_id = CourseRepository.insert_course(course_data)
                self.load_courses()
                QMessageBox.information(self, "Success", f"Course {new_id} added!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def handle_update(self):
        row = self.ui.table_quanly.currentRow()
        if row >= 0:
            col_count = self.ui.table_quanly.columnCount()
            old = [self.ui.table_quanly.item(row, i).text() if self.ui.table_quanly.item(row, i) else "" for i in range(col_count)]
            res = self.show_input_form("Edit Course", old)
            if res:
                try:
                    # Schema: (course_id, course_name, description, level, duration_weeks, tuition_fee, status)
                    course_data = (
                        res["id"],
                        res["name"],
                        res["desc"],
                        res["level"],
                        res["duration"],
                        res["fee"],
                        res["status"]
                    )
                    CourseRepository.update_course(course_data)
                    self.load_courses()
                    QMessageBox.information(self, "Success", "Course updated!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def handle_delete(self):
        row = self.ui.table_quanly.currentRow()
        if row >= 0:
            course_id = self.ui.table_quanly.item(row, 0).text()
            if QMessageBox.question(self, "Delete", f"Delete course {course_id}?") == QMessageBox.StandardButton.Yes:
                CourseRepository.delete_course(course_id)
                self.load_courses()
