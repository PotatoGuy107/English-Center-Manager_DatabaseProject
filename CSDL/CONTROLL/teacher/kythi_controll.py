from PyQt6.QtWidgets import QDialog
from gdien.chonkythi import Ui_Dialog
from CONTROLL.teacher.nhapdiem_controll import NhapDiem

class TeacherChonKyThi(QDialog):
    def __init__(self, ma_lop, parent=None):
        super().__init__(parent)


        self.ma_lop = ma_lop

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Hiển thị mã lớp
        self.ui.Malop1.setText(ma_lop)

        # Nút Trở về
        self.ui.trove1.clicked.connect(self.go_back)
        self.ui.giuakhoa.clicked.connect(lambda: self.open_nhapdiem("Giữa khóa"))
        self.ui.cuoikhoa.clicked.connect(lambda: self.open_nhapdiem("Cuối khóa"))

    
    def open_cuoi_ky(self):
        self.open_nhapdiem("Cuối khóa")

    def open_nhapdiem(self, ky_thi):
        self.hide()  # Ẩn màn hình cũ

        self.nhapdiem = NhapDiem(self.ma_lop, ky_thi)
        self.nhapdiem.exec()

        self.show()
    def go_back(self):
        self.close()
        if self.parent():
            self.parent().show()