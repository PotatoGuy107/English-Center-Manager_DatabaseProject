from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

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

        self.ui.danhsachhocvien.setRowCount(len(students))
        for row, s in enumerate(students):
            self.ui.danhsachhocvien.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.ui.danhsachhocvien.setItem(row, 1, QTableWidgetItem(s.student_id))
            self.ui.danhsachhocvien.setItem(row, 2, QTableWidgetItem(s.name))
            self.ui.danhsachhocvien.setItem(row, 3, QTableWidgetItem(s.birth.toString("dd/MM/yyyy")))
            score_value = score_dict.get(s.student_id, "")
            score_item = QTableWidgetItem(str(score_value))
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
