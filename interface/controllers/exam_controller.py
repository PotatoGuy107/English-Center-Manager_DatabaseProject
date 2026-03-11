from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from interface.views.generated.create_exam_ui import Ui_Dialog
from application.use_cases.exam_use_cases import ExamUseCases

# Common input styling
INPUT_STYLE = """
    QLineEdit, QTextEdit {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
"""

COMBO_STYLE = """
    QComboBox {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QComboBox:focus {
        border: 2px solid #8b0000;
    }
    QComboBox QAbstractItemView {
        background-color: white;
        color: #222;
        selection-background-color: #bc1823;
        selection-color: white;
    }
"""

DATE_STYLE = """
    QDateEdit {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QDateEdit:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
    QDateEdit::drop-down {
        border: none;
        width: 25px;
    }
"""


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

        # Apply input styling
        self.ui.loaikythi.setStyleSheet(COMBO_STYLE)
        self.ui.ngaythi.setStyleSheet(DATE_STYLE)
        self.ui.textmota.setStyleSheet(INPUT_STYLE)
        
        # Set current date
        self.ui.ngaythi.setDate(QDate.currentDate())

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
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn loại kỳ thi")
            return

        try:
            exam_id = ExamUseCases.create_exam(
                self.class_id, exam_type, exam_date, description
            )
            
            QMessageBox.information(
                self, "Thành công",
                f"Tạo kỳ thi '{exam_type}' thành công!\n"
                f"Mã kỳ thi: {exam_id}\nNgày thi: {exam_date}",
            )
            self.go_back()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo kỳ thi: {str(e)}")
