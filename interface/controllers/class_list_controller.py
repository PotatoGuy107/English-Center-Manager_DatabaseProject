from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QBrush, QColor

from interface.views.generated.class_list_ui import Ui_Dialog
from application.use_cases.class_list_use_cases import ClassListUseCases


def _make_item(text):
    item = QTableWidgetItem(str(text))
    item.setForeground(QBrush(QColor("#222")))
    return item


class ClassListController(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.selected_class_code = None
        self.student_list_window = None
        self.use_cases = ClassListUseCases()

        self.connect_signals()
        self.load_data()

    def connect_signals(self):
        self.ui.return_2.clicked.connect(self.go_back)
        self.ui.taokythi.clicked.connect(self.open_exam)
        self.ui.addhv.clicked.connect(self.open_add_student)
        self.ui.dslopqli.itemSelectionChanged.connect(self.get_selected_class)
        self.ui.xemdshv.clicked.connect(self.open_student_list)
        self.ui.qlyhcphi.clicked.connect(self.open_payment)

    def load_data(self):
        data = self.use_cases.get_all_classes()
        table = self.ui.dslopqli
        table.setAlternatingRowColors(False)
        table.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
        table.setRowCount(0)
        for c in data:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, _make_item(row + 1))
            table.setItem(row, 1, _make_item(c.code))
            table.setItem(row, 2, _make_item(c.name))
            table.setItem(row, 3, _make_item(c.course))
            table.setItem(row, 4, _make_item(c.teacher))
            table.setItem(
                row, 5,
                _make_item(
                    f"{c.start_date.toString('dd/MM/yyyy')} - {c.end_date.toString('dd/MM/yyyy')}"
                ),
            )
            table.setItem(row, 6, _make_item(c.progress))
            table.setItem(row, 7, _make_item(c.status))

    def get_selected_class(self):
        selected = self.ui.dslopqli.selectedItems()
        if selected:
            row = selected[0].row()
            self.selected_class_code = self.ui.dslopqli.item(row, 1).text()
        else:
            self.selected_class_code = None

    def open_student_list(self):
        if not self.selected_class_code:
            QMessageBox.warning(self, "No class selected", "Please select a class first")
            return
        from interface.controllers.student_list_controller import StudentListController
        if self.student_list_window is None:
            self.student_list_window = StudentListController(self.selected_class_code)
        else:
            self.student_list_window.set_class(self.selected_class_code)
            self.student_list_window.load_students()
        self.student_list_window.show()

    def open_add_student(self):
        if not self.selected_class_code:
            QMessageBox.warning(self, "No class selected", "Please select a class first")
            return
        table = self.ui.dslopqli
        row = table.currentRow()
        if row < 0:
            return
        enrollment_item = table.item(row, 6)
        status_item = table.item(row, 7)
        if not enrollment_item or not status_item:
            QMessageBox.warning(self, "Error", "Missing class data")
            return
        enrollment = enrollment_item.text().strip()
        status = status_item.text().strip().lower()
        if "đang học" in status or "đã khai giảng" in status:
            QMessageBox.warning(self, "Cannot add", "Class already started. Cannot add students.")
            return
        try:
            current, max_students = enrollment.split("/")
            if int(current) >= int(max_students):
                QMessageBox.warning(self, "Class full", f"Class is at capacity ({enrollment})")
                return
        except Exception:
            QMessageBox.warning(self, "Data error", f"Invalid enrollment data: {enrollment}")
            return
        from interface.controllers.add_student_controller import AddStudentController
        self.add_student_window = AddStudentController(self.selected_class_code)
        self.add_student_window.exec()
        self.load_data()

    def open_exam(self):
        if not self.selected_class_code:
            QMessageBox.warning(self, "No class selected", "Please select a class first")
            return
        row = self.ui.dslopqli.currentRow()
        if row < 0:
            return
        class_code = self.ui.dslopqli.item(row, 1).text()
        class_name = self.ui.dslopqli.item(row, 2).text()
        self.hide()
        from interface.controllers.exam_controller import ExamController
        dlg = ExamController(class_code, class_name, self)
        dlg.exec()

    def open_payment(self):
        if not self.selected_class_code:
            QMessageBox.warning(self, "No class selected", "Please select a class first")
            return
        self.hide()
        from interface.controllers.payment_controller import PaymentController
        self.payment_window = PaymentController(self.selected_class_code, self)
        self.payment_window.show()

    def go_back(self):
        from interface.controllers.class_controller import ClassController
        self.main_window = ClassController()
        self.main_window.show()
        self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()
