from PyQt6.QtWidgets import QDialog

from interface.views.generated.select_exam_ui import Ui_Dialog


class TeacherExamController(QDialog):
    def __init__(self, class_code, parent=None):
        super().__init__(parent)
        self.class_code = class_code
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.Malop1.setText(class_code)
        self.ui.trove1.clicked.connect(self.go_back)
        self.ui.giuakhoa.clicked.connect(lambda: self.open_grade_entry("Giữa khóa"))
        self.ui.cuoikhoa.clicked.connect(lambda: self.open_grade_entry("Cuối khóa"))

    def open_grade_entry(self, exam_type):
        self.hide()
        from interface.controllers.teacher.grade_entry_controller import GradeEntryController
        self.grade_entry = GradeEntryController(self.class_code, exam_type)
        self.grade_entry.exec()
        self.show()

    def go_back(self):
        self.close()
        if self.parent():
            self.parent().show()
