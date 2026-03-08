from PyQt6.QtWidgets import QDialog, QMessageBox
from interface.views.generated.create_exam_ui import Ui_Dialog
from infrastructure.repositories.exam_repository import ExamRepository


class ExamController(QDialog):
    def __init__(self, class_id, class_name, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_id = class_id
        self.class_name = class_name

        self.ui.lophoc.setText(class_name)
        self.ui.Malop1_2.setText(str(class_id))

        self.ui.Button_return_2.clicked.connect(self.go_back)
        self.ui.btnhuy2.clicked.connect(self.go_back)
        self.ui.btncreate.clicked.connect(self.create_exam)

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def create_exam(self):
        exam_type = self.ui.loaikythi.currentText()
        exam_date = self.ui.ngaythi.date().toString("yyyy-MM-dd")
        description = self.ui.textmota.toPlainText()

        if exam_type == "--Choose--":
            QMessageBox.warning(self, "Error", "Please select exam type")
            return

        try:
            # Save to database
            exam_data = (self.class_id, exam_type, exam_date, description)
            exam_id = ExamRepository.insert(exam_data)
            
            QMessageBox.information(
                self, "Success",
                f"Exam '{exam_type}' created successfully!\n"
                f"Exam ID: {exam_id}\nDate: {exam_date}",
            )
            self.go_back()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create exam: {str(e)}")
