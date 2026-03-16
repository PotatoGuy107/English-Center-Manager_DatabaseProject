from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QBrush, QColor

from interface.views.generated.add_student_ui import Ui_Dialog
from application.use_cases.add_student_use_cases import AddStudentUseCases

# Common input styling for visibility
INPUT_STYLE = """
    QLineEdit {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QLineEdit:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
    QLineEdit::placeholder {
        color: #999;
    }
"""


class AddStudentController(QDialog):
    def __init__(self, class_code):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.use_cases = AddStudentUseCases()

        self.ui.Malop1.setText(class_code)
        
        # Apply input styling
        self.ui.txtSearch1.setStyleSheet(INPUT_STYLE)
        
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
        dob_str = s.date_of_birth.strftime("%d/%m/%Y") if hasattr(s, "date_of_birth") and hasattr(s.date_of_birth, "strftime") else str(getattr(s, "date_of_birth", ""))
        reg_date_str = s.register_date.strftime("%d/%m/%Y") if hasattr(s, "register_date") and hasattr(s.register_date, "strftime") else str(getattr(s, "register_date", ""))
        
        items = [
            QTableWidgetItem(str(index + 1)),
            QTableWidgetItem(str(getattr(s, "student_id", ""))),
            QTableWidgetItem(str(getattr(s, "full_name", ""))),
            QTableWidgetItem(dob_str),
            QTableWidgetItem(str(getattr(s, "gender", ""))),
            QTableWidgetItem(str(getattr(s, "address", ""))),
            QTableWidgetItem(str(getattr(s, "phone_number", ""))),
            QTableWidgetItem(str(getattr(s, "email", ""))),
            QTableWidgetItem(reg_date_str)
        ]
        for col, item in enumerate(items):
            item.setForeground(QBrush(QColor("#222")))
            table.setItem(row, col, item)

    def load_students(self):
        students = self.use_cases.get_students_by_class(self.class_code)
        table = self.ui.themhv
        table.setAlternatingRowColors(False)
        table.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
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
