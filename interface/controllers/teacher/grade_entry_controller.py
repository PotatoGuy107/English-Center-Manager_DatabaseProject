from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor

from interface.views.generated.grade_entry_ui import Ui_Dialog
from application.use_cases.teacher.grade_entry_use_cases import GradeEntryUseCases


class GradeEntryController(QDialog):
    def __init__(self, class_code, exam_type):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.exam_type = exam_type
        self.use_cases = GradeEntryUseCases()

        self.ui.labelmalop.setText(class_code)
        self.ui.ky_thi.setText(exam_type)

        self.ui.btnsua_2.clicked.connect(self.save_scores)
        self.ui.btnsua.clicked.connect(self.enable_editing)
        self.ui.Button_return.clicked.connect(self.close)

        self.load_data()

    def load_data(self):
        students = self.use_cases.get_students_by_class(self.class_code)
        scores = self.use_cases.get_scores(self.class_code, self.exam_type)
        score_dict = {s.student_id: s.score for s in scores}

        self.ui.danhsachhocvien.setAlternatingRowColors(False)
        self.ui.danhsachhocvien.setStyleSheet("""
            QTableWidget { background-color: white; color: #222; gridline-color: #ccc; }
            QTableWidget::item { color: #222; padding: 5px; background-color: white; }
            QTableWidget::item:selected { background-color: #bc1823; color: white; }
            QHeaderView::section { background-color: #bc1823; color: white; font-weight: bold; padding: 5px; }
        """)
        self.ui.danhsachhocvien.setRowCount(len(students))
        for row, s in enumerate(students):
            item = QTableWidgetItem(str(row + 1))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.danhsachhocvien.setItem(row, 0, item)
            item = QTableWidgetItem(str(s.student_id))
            item.setForeground(QBrush(QColor("#222")))
            self.ui.danhsachhocvien.setItem(row, 1, item)
            item = QTableWidgetItem(s.full_name or "")
            item.setForeground(QBrush(QColor("#222")))
            self.ui.danhsachhocvien.setItem(row, 2, item)
            dob_str = s.date_of_birth.strftime("%d/%m/%Y") if s.date_of_birth else ""
            item = QTableWidgetItem(dob_str)
            item.setForeground(QBrush(QColor("#222")))
            self.ui.danhsachhocvien.setItem(row, 3, item)
            score_value = score_dict.get(s.student_id, "")
            score_item = QTableWidgetItem(str(score_value))
            score_item.setForeground(QBrush(QColor("#222")))
            score_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEditable |
                Qt.ItemFlag.ItemIsEnabled
            )
            self.ui.danhsachhocvien.setItem(row, 4, score_item)

    def enable_editing(self):
        table = self.ui.danhsachhocvien
        current_row = table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Info", "Please select a student!")
            return
        table.setEditTriggers(table.EditTrigger.AllEditTriggers)
        table.setCurrentCell(current_row, 4)
        table.editItem(table.currentItem())

    def save_scores(self):
        row_count = self.ui.danhsachhocvien.rowCount()
        for row in range(row_count):
            student_id = self.ui.danhsachhocvien.item(row, 1).text()
            score_item = self.ui.danhsachhocvien.item(row, 4)
            if score_item is None:
                continue
            score_text = score_item.text().strip()
            if score_text == "":
                continue
            try:
                score = float(score_text)
            except ValueError:
                QMessageBox.warning(self, "Error", f"Invalid score at row {row + 1}")
                return
            self.use_cases.save_score(self.class_code, student_id, self.exam_type, score)
        QMessageBox.information(self, "Success", "Scores saved successfully!")
        self.ui.danhsachhocvien.setEditTriggers(
            self.ui.danhsachhocvien.EditTrigger.NoEditTriggers
        )
