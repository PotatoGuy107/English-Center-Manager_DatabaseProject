from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal
from gdien.classlist import Ui_Dialog
from CONTROLL.teacher.kythi_controll import TeacherChonKyThi
from BILL.teacher.classlist_bll import ClasslistBLL

class TeacherClassList(QDialog):
    logout_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.bll = ClasslistBLL()
        self.load_classes()

        # Khi bấm nút Nhập điểm
        self.ui.nhapdiem.clicked.connect(self.open_chonkythi)
        self.ui.dangxuat.clicked.connect(self.logout)
        # Nếu muốn nhấn Enter cũng mở
        self.ui.danhsachlopday.itemActivated.connect(self.open_chonkythi)

    def logout(self):
        self.logout_requested.emit()   # phát tín hiệu
                        # đóng cửa sổ hiện tại

    def load_classes(self):
        classes = self.bll.get_all_classes()

        table = self.ui.danhsachlopday
        table.setRowCount(0)

        for row, c in enumerate(classes):
            table.insertRow(row)

            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QTableWidgetItem(c.code))
            table.setItem(row, 2, QTableWidgetItem(c.name))

            # Cột 3 - Khóa
            table.setItem(row, 3, QTableWidgetItem(c.course))

            # Cột 4 - Số HV
            table.setItem(row, 4, QTableWidgetItem(str(c.max_class)))

            # Cột 5 - Trạng thái 
            
            table.setItem(row, 5, QTableWidgetItem(c.status))


    def open_chonkythi(self):
        selected_items = self.ui.danhsachlopday.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một lớp!")
            return

        selected_row = self.ui.danhsachlopday.currentRow()

        ma_lop_item = self.ui.danhsachlopday.item(selected_row, 1)

        if ma_lop_item is None:
            QMessageBox.warning(self, "Lỗi", "Không lấy được mã lớp!")
            return

        ma_lop = ma_lop_item.text()
        self.hide()
        self.chonkythi_window = TeacherChonKyThi(ma_lop, parent=self)
        self.chonkythi_window.show()
