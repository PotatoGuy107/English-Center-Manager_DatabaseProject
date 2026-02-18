
from gdien.dslopp import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem

from DAL.dslop_dal import FakeClassRepository


from CONTROLL.dshocvien_controller import DanhSachHocVienController




class DanhSachLopController(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.selected_class_code = None 
        self.dshv_window = None

        self.connect_signals()
        self.load_data()



    def connect_signals(self):
        self.ui.return_2.clicked.connect(self.go_back)

        self.ui.addhv.clicked.connect(self.open_themhocvien)
        self.ui.dslopqli.itemSelectionChanged.connect(self.get_selected_class)
        self.ui.xemdshv.clicked.connect(self.open_dshv)
      
    
    def go_back(self):
        from CONTROLL.controllclass import TaoLopController

        self.main_window = TaoLopController()
        self.main_window.show()

        self.close()


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
        print("ĐÃ CLICK NÚT THÊM HV")

        from CONTROLL.themhocvien_controller import ThemHocVienController

        table = self.ui.dslopqli
        row = table.currentRow()

        print("ROW =", row)
        print("selected_class_code =", self.selected_class_code)

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
                "Lớp đã khai giảng / đang học\nKhông được thêm học viên"
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

        # mở form thêm học viên
        self.themhocvien_window = ThemHocVienController(self.selected_class_code)
        self.themhocvien_window.exec()


    def load_data(self):
        repo = FakeClassRepository()
        data = repo.get_all_classes()

        table = self.ui.dslopqli
        table.setRowCount(0)

        for row_data in data:
            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, tableItem(str(row + 1)))
            table.setItem(row, 1, tableItem(row_data[0]))
            table.setItem(row, 2, tableItem(row_data[1]))
            table.setItem(row, 3, tableItem(row_data[2]))
            table.setItem(row, 4, tableItem(row_data[3]))
            table.setItem(row, 5, tableItem(row_data[4]))
            table.setItem(row, 6, tableItem(row_data[5]))
            table.setItem(row, 7, tableItem(row_data[6]))


def tableItem(text):
    return QTableWidgetItem(text)
