
from gdien.dslopp import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem

from BILL.dslop_bll import DSLopBLL

from CONTROLL.dshocvien_controller import DanhSachHocVienController
from CONTROLL.taokythi_controll import TaoKyThiController
from CONTROLL.thanhtoan_controller import ManHinhThanhToanController

class DanhSachLopController(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.selected_class_code = None
        self.dshv_window = None

        self.bll = DSLopBLL()   

        self.connect_signals()
        self.load_data()


    def connect_signals(self):
        self.ui.return_2.clicked.connect(self.go_back)
        self.ui.taokythi.clicked.connect(self.open_taokythi)
        self.ui.addhv.clicked.connect(self.open_themhocvien)
        self.ui.dslopqli.itemSelectionChanged.connect(self.get_selected_class)
        self.ui.xemdshv.clicked.connect(self.open_dshv)
        self.ui.qlyhcphi.clicked.connect(self.open_thanhtoan)

  
    def load_data(self):
        data = self.bll.get_all_classes()  

        table = self.ui.dslopqli
        table.setRowCount(0)

        for c in data:
            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, tableItem(str(row + 1)))
            table.setItem(row, 1, tableItem(c.code))
            table.setItem(row, 2, tableItem(c.name))
            table.setItem(row, 3, tableItem(c.course))
            table.setItem(row, 4, tableItem(c.teacher))
            table.setItem(
                row,
                5,
                tableItem(
                    f"{c.start_date.toString('dd/MM/yyyy')} - "
                    f"{c.end_date.toString('dd/MM/yyyy')}"
                ),
            )
            table.setItem(row, 6, tableItem(c.progress))
            table.setItem(row, 7, tableItem(c.status))


    def get_selected_class(self):
        table = self.ui.dslopqli
        selected = table.selectedItems()

        if selected:
            row = selected[0].row()
            self.selected_class_code = table.item(row, 1).text()
        else:
            self.selected_class_code = None

 
    def open_dshv(self):
        if not self.selected_class_code:
            QMessageBox.warning(self, "Chưa chọn lớp", "Vui lòng chọn lớp trước")
            return

        if self.dshv_window is None:
            self.dshv_window = DanhSachHocVienController(self.selected_class_code)
        else:
            self.dshv_window.set_class(self.selected_class_code)
            self.dshv_window.load_students()

        self.dshv_window.show()


    def open_themhocvien(self):
        from CONTROLL.themhocvien_controller import ThemHocVienController

        table = self.ui.dslopqli
        row = table.currentRow()

        if row < 0 or not self.selected_class_code:
            QMessageBox.warning(self, "Chưa chọn lớp", "Vui lòng chọn lớp trước")
            return

        si_so_item = table.item(row, 6)
        trang_thai_item = table.item(row, 7)

        if not si_so_item or not trang_thai_item:
            QMessageBox.warning(self, "Lỗi", "Thiếu dữ liệu lớp")
            return

        si_so = si_so_item.text().strip()
        trang_thai = trang_thai_item.text().strip().lower()

        # Không cho thêm nếu lớp đang học
        if "đang học" in trang_thai or "đã khai giảng" in trang_thai:
            QMessageBox.warning(
                self,
                "Không thể thêm",
                "Lớp đã khai giảng / đang học\nKhông được thêm học viên",
            )
            return

        try:
            current, max_student = si_so.split("/")
            current = int(current)
            max_student = int(max_student)

            if current >= max_student:
                QMessageBox.warning(self, "Lớp đã đủ", f"Sĩ số lớp đã đủ ({si_so})")
                return

        except Exception as e:
            QMessageBox.warning(self, "Lỗi dữ liệu", f"Sĩ số không hợp lệ: {si_so}")
            print("ERROR:", e)
            return

        self.themhocvien_window = ThemHocVienController(self.selected_class_code)
        self.themhocvien_window.exec()
        self.load_data()

    def open_taokythi(self):
        if not self.selected_class_code:
            QMessageBox.warning(
                self,
                "Chưa chọn lớp",
                "Vui lòng chọn lớp trước khi tạo kỳ thi",
            )
            return

        row = self.ui.dslopqli.currentRow()
        if row < 0:
            return

        class_code = self.ui.dslopqli.item(row, 1).text()
        class_name = self.ui.dslopqli.item(row, 2).text()

        self.hide()

        dlg = TaoKyThiController(class_code, class_name, self)
        dlg.exec()
    
    def open_thanhtoan(self):
        if not self.selected_class_code:
            QMessageBox.warning(
                self,
                "Chưa chọn lớp",
                "Vui lòng chọn lớp trước khi quản lý học phí",
            )
            return

        self.hide()

        self.thanhtoan_window = ManHinhThanhToanController(
            self.selected_class_code,
            self
        )
        self.thanhtoan_window.show()


    def go_back(self):
        from CONTROLL.controllclass import TaoLopController

        self.main_window = TaoLopController()
        self.main_window.show()
        self.close()


    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()



def tableItem(text):
    return QTableWidgetItem(str(text))