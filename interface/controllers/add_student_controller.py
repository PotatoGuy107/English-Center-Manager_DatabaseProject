from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate

from interface.views.generated.add_student_ui import Ui_Dialog
from application.use_cases.add_student_use_cases import AddStudentUseCases


class AddStudentController(QDialog):
    def __init__(self, class_code):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.use_cases = AddStudentUseCases()

        self.ui.Malop1.setText(class_code)
        self.connect_signals()
        self.load_students()

    def connect_signals(self):
        self.ui.search1.clicked.connect(self.search_student)
        self.ui.btnsua_2.clicked.connect(self.save_students)
        self.ui.Button_return.clicked.connect(self.close)
        self.ui.btnthem.clicked.connect(self.add_row)
        self.ui.btnxoa.clicked.connect(self.delete_row)

    def fill_row(self, row, index, s):
        table = self.ui.themhv
        table.setItem(row, 0, QTableWidgetItem(str(index + 1)))
        table.setItem(row, 1, QTableWidgetItem(s.student_id))
        table.setItem(row, 2, QTableWidgetItem(s.name))
        table.setItem(row, 3, QTableWidgetItem(s.birth.toString("dd/MM/yyyy")))
        table.setItem(row, 4, QTableWidgetItem(s.gender))
        table.setItem(row, 5, QTableWidgetItem(s.address))
        table.setItem(row, 6, QTableWidgetItem(s.phone))
        table.setItem(row, 7, QTableWidgetItem(s.email))
        table.setItem(row, 8, QTableWidgetItem(s.register_date.toString("dd/MM/yyyy")))

    def load_students(self):
        students = self.use_cases.get_students_by_class(self.class_code)
        table = self.ui.themhv
        table.setRowCount(0)
        for i, s in enumerate(students):
            row = table.rowCount()
            table.insertRow(row)
            self.fill_row(row, i, s)

    def search_student(self):
        keyword = self.ui.txtSearch1.text().strip()
        if not keyword:
            self.load_students()
            return
        students = self.use_cases.search_students(self.class_code, keyword)
        table = self.ui.themhv
        table.setRowCount(0)
        for i, s in enumerate(students):
            row = table.rowCount()
            table.insertRow(row)
            self.fill_row(row, i, s)

    def save_students(self):
        table = self.ui.themhv
        for row in range(table.rowCount()):
            name_item = table.item(row, 2)
            if not name_item or not name_item.text().strip():
                continue
            id_item = table.item(row, 1)
            student_id = id_item.text().strip() if id_item else ""
            name = name_item.text()
            birth_text = table.item(row, 3).text() if table.item(row, 3) else ""
            birth = QDate.fromString(birth_text, "dd/MM/yyyy")
            gender = table.item(row, 4).text() if table.item(row, 4) else ""
            address = table.item(row, 5).text() if table.item(row, 5) else ""
            phone = table.item(row, 6).text() if table.item(row, 6) else ""
            email = table.item(row, 7).text() if table.item(row, 7) else ""
            result = self.use_cases.save_student(
                self.class_code, student_id, name, birth, gender, address, phone, email
            )
            if isinstance(result, str):
                table.setItem(row, 1, QTableWidgetItem(result))
        QMessageBox.information(self, "OK", "Data saved")
        self.load_students()

    def add_row(self):
        table = self.ui.themhv
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        for col in range(1, 9):
            table.setItem(row, col, QTableWidgetItem(""))

    def delete_row(self):
        table = self.ui.themhv
        row = table.currentRow()
        if row < 0:
            return
        id_item = table.item(row, 1)
        if id_item and id_item.text().strip():
            self.use_cases.delete_student(id_item.text().strip())
        table.removeRow(row)
        for i in range(table.rowCount()):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
