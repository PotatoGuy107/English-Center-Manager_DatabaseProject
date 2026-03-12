from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QBrush, QColor

from interface.views.generated.teacher_class_ui import Ui_Dialog
from application.use_cases.teacher.class_list_use_cases import TeacherClassListUseCases


class TeacherClassListController(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.teacher_id = None  # Current teacher's ID

        self.use_cases = TeacherClassListUseCases()

        self.ui.nhapdiem.clicked.connect(self.open_select_exam)
        self.ui.dangxuat.clicked.connect(self.handle_logout)
        self.ui.danhsachlopday.itemDoubleClicked.connect(self.open_select_exam)

    def set_teacher_id(self, teacher_id: str):
        """Set teacher ID and reload classes"""
        self.teacher_id = teacher_id
        self.load_classes()

    def handle_logout(self):
        self.logout_requested.emit()

    def load_classes(self):
        """Load classes for current teacher"""
        if self.teacher_id:
            classes = self.use_cases.get_classes_by_teacher(self.teacher_id)
        else:
            classes = self.use_cases.get_all_classes()
        
        table = self.ui.danhsachlopday
        table.setAlternatingRowColors(False)
        table.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
        table.setRowCount(0)
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["STT", "Mã lớp", "Tên lớp", "Khóa", "Số HV", "Trạng thái"])
        
        for row, c in enumerate(classes):
            table.insertRow(row)
            item = QTableWidgetItem(str(row + 1))
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, 0, item)
            # c is tuple: (class_id, class_name, skill_name, start_date, end_date, status)
            item = QTableWidgetItem(str(c[0]))
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, 1, item)  # class_id
            item = QTableWidgetItem(str(c[1]))
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, 2, item)  # class_name
            item = QTableWidgetItem(str(c[2] or ""))
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, 3, item)  # skill_name
            # For max_student count, we would need to query - for now show "-"
            item = QTableWidgetItem("-")
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, 4, item)
            item = QTableWidgetItem(str(c[5] or ""))
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, 5, item)  # status

    def open_select_exam(self):
        selected_items = self.ui.danhsachlopday.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một lớp!")
            return
        selected_row = self.ui.danhsachlopday.currentRow()
        class_code_item = self.ui.danhsachlopday.item(selected_row, 1)
        if class_code_item is None:
            QMessageBox.warning(self, "Lỗi", "Không thể lấy mã lớp!")
            return
        class_code = class_code_item.text()
        self.hide()
        from interface.controllers.teacher.exam_controller import TeacherExamController
        self.exam_window = TeacherExamController(class_code, parent=self)
        self.exam_window.show()
