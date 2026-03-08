from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

from interface.views.generated.student_list_ui import Ui_Dialog
from application.use_cases.student_use_cases import StudentUseCases


class StudentListController(QDialog):
    def __init__(self, class_code):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.ui.Malop.setText(class_code)

        self.use_cases = StudentUseCases()
        self.connect_signals()
        self.init_table()
        self.load_students()

    def set_class(self, class_code):
        self.class_code = class_code
        self.load_students()

    def connect_signals(self):
        self.ui.Button_return.clicked.connect(self.close)
        self.ui.search.clicked.connect(self.search_student)
        self.ui.btnsua.clicked.connect(self.enable_editing)
        self.ui.btnluu.clicked.connect(self.save_edit)

    def init_table(self):
        table = self.ui.dshv
        table.setRowCount(0)
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)

    def fill_table(self, students):
        table = self.ui.dshv
        table.setRowCount(0)
        for student in students:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QTableWidgetItem(student.student_id))
            table.setItem(row, 2, QTableWidgetItem(student.name))
            table.setItem(row, 3, QTableWidgetItem(student.birth.toString("dd/MM/yyyy")))
            table.setItem(row, 4, QTableWidgetItem(student.gender))
            table.setItem(row, 5, QTableWidgetItem(student.address))
            table.setItem(row, 6, QTableWidgetItem(student.phone))
            table.setItem(row, 7, QTableWidgetItem(student.email))
            table.setItem(row, 8, QTableWidgetItem(student.register_date.toString("dd/MM/yyyy")))

    def load_students(self):
        students = self.use_cases.get_students_by_class(self.class_code)
        self.fill_table(students)

    def search_student(self):
        keyword = self.ui.txtSearch.text().strip()
        if not keyword:
            self.load_students()
            return
        students = self.use_cases.search_students(self.class_code, keyword)
        self.fill_table(students)

    def enable_editing(self):
        table = self.ui.dshv
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Please select a student")
            return
        self.editing_row = row
        table.setEditTriggers(
            table.EditTrigger.DoubleClicked | table.EditTrigger.SelectedClicked
        )
        self._lock_columns(row)
        self._highlight_row(row)
        QMessageBox.information(self, "Edit mode", "You can now edit the selected row")

    def _lock_columns(self, row):
        table = self.ui.dshv
        for col in [0, 1]:
            item = table.item(row, col)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    def _highlight_row(self, row):
        table = self.ui.dshv
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(Qt.GlobalColor.yellow)

    def save_edit(self):
        if not hasattr(self, "editing_row"):
            QMessageBox.warning(self, "Error", "No row selected for editing")
            return
        row = self.editing_row
        table = self.ui.dshv
        try:
            student_id = table.item(row, 1).text()
            name = table.item(row, 2).text()
            phone = table.item(row, 6).text()
            email = table.item(row, 7).text()
        except AttributeError:
            QMessageBox.warning(self, "Error", "Invalid data")
            return
        valid, message = StudentUseCases.validate_student(name, phone, email)
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        updated = self.use_cases.update_student(student_id, name, phone, email)
        if updated:
            QMessageBox.information(self, "OK", "Student updated successfully")
        else:
            QMessageBox.warning(self, "Error", "Student not found")
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)
        del self.editing_row
        self.load_students()
