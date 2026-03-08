from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal

from interface.views.generated.teacher_class_ui import Ui_Dialog
from application.use_cases.teacher.class_list_use_cases import TeacherClassListUseCases


class TeacherClassListController(QDialog):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.use_cases = TeacherClassListUseCases()
        self.load_classes()

        self.ui.nhapdiem.clicked.connect(self.open_select_exam)
        self.ui.dangxuat.clicked.connect(self.handle_logout)
        self.ui.danhsachlopday.itemActivated.connect(self.open_select_exam)

    def handle_logout(self):
        self.logout_requested.emit()

    def load_classes(self):
        classes = self.use_cases.get_all_classes()
        table = self.ui.danhsachlopday
        table.setRowCount(0)
        for row, c in enumerate(classes):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            # c is tuple: (class_id, class_name, course_name, skill_name, teacher_id, start_date, end_date, max_student, status)
            table.setItem(row, 1, QTableWidgetItem(str(c[0])))  # class_id
            table.setItem(row, 2, QTableWidgetItem(str(c[1])))  # class_name
            table.setItem(row, 3, QTableWidgetItem(str(c[2] or "")))  # course_name
            table.setItem(row, 4, QTableWidgetItem(str(c[7] or 0)))  # max_student
            table.setItem(row, 5, QTableWidgetItem(str(c[8] or "")))  # status

    def open_select_exam(self):
        selected_items = self.ui.danhsachlopday.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Info", "Please select a class!")
            return
        selected_row = self.ui.danhsachlopday.currentRow()
        class_code_item = self.ui.danhsachlopday.item(selected_row, 1)
        if class_code_item is None:
            QMessageBox.warning(self, "Error", "Could not retrieve class code!")
            return
        class_code = class_code_item.text()
        self.hide()
        from interface.controllers.teacher.exam_controller import TeacherExamController
        self.exam_window = TeacherExamController(class_code, parent=self)
        self.exam_window.show()
