from PyQt6.QtWidgets import QDialog, QMessageBox
from gdien.taokythi import Ui_Dialog


class TaoKyThiController(QDialog):
    def __init__(self, class_code, class_name,parent=None):
        super().__init__(parent)

        self.parent_window = parent

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.class_name = class_name

        self.ui.lophoc.setText(class_name)
        self.ui.Malop1_2.setText(class_code)

        self.connect_signals()

    def connect_signals(self):
        self.ui.Button_return_2.clicked.connect(self.go_back)
        self.ui.btnhuy2.clicked.connect(self.go_back)
        self.ui.btncreate.clicked.connect(self.create_exam)

    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def create_exam(self):
        loai = self.ui.loaikythi.currentText()
        ngay = self.ui.ngaythi.date().toString("dd/MM/yyyy")
        mota = self.ui.textmota.toPlainText()

        if loai == "--Choose--":
            QMessageBox.warning(self, "Lỗi", "Chọn loại kỳ thi")
            return

        QMessageBox.information(
            self,
            "Thành công",
            f"Tạo thành công kỳ thi {loai} cho lớp {self.class_code}\n"
              f"Ngày thi: {ngay}\n"
            f"Mô tả: {mota}"
        )

        self.go_back()