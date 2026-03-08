from PyQt6.QtWidgets import QDialog, QMessageBox
from interface.views.generated.create_exam_ui import Ui_Dialog


class ExamController(QDialog):
    def __init__(self, class_code, class_name, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.class_name = class_name

        self.ui.lophoc.setText(class_name)
        self.ui.Malop1_2.setText(class_code)

        self.ui.Button_return_2.clicked.connect(self.go_back)
        self.ui.btnhuy2.clicked.connect(self.go_back)
        self.ui.btncreate.clicked.connect(self.create_exam)

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def create_exam(self):
        exam_type = self.ui.loaikythi.currentText()
        exam_date = self.ui.ngaythi.date().toString("dd/MM/yyyy")
        description = self.ui.textmota.toPlainText()

        if exam_type == "--Choose--":
            QMessageBox.warning(self, "Error", "Please select exam type")
            return

        QMessageBox.information(
            self, "Success",
            f"Exam '{exam_type}' created for class {self.class_code}\n"
            f"Date: {exam_date}\nDescription: {description}",
        )
        self.go_back()
