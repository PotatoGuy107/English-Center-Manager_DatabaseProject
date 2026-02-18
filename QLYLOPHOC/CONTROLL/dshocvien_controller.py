from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

from gdien.dshocvienn import Ui_Dialog
from DAL.dshv_dal import FakeStudentRepository
from BILL.dshv_bll import DSHocVienBLL



class DanhSachHocVienController(QDialog):
    def __init__(self, class_code):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.ui.Malop.setText(class_code)

        self.connect_signals()

        self.repo = FakeStudentRepository()
        self.init_table()
        self.load_students()

        self.class_code = class_code

    def set_class(self, class_code):
        self.class_code = class_code
        self.load_students()


    
    def connect_signals(self):
        self.ui.Button_return.clicked.connect(self.close)
        self.ui.search.clicked.connect(self.search_student)
        self.ui.btnsua.clicked.connect(self.enable_editing)
        self.ui.btnluu.clicked.connect(self.save_edit)
    def init_table(self):
        table = self.ui.dshv
        table.setRowCount(0)
        table.setEditTriggers(table.EditTrigger.NoEditTriggers)


    def fill_table(self, students):

        table = self.ui.dshv
        table.setRowCount(0)

        for student in students:

            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QTableWidgetItem(student.student_id))
            table.setItem(row, 2, QTableWidgetItem(student.name))
            table.setItem(row, 3, QTableWidgetItem(student.birth.toString("dd/MM/yyyy")))
            table.setItem(row, 4, QTableWidgetItem(student.gender))
            table.setItem(row, 5, QTableWidgetItem(student.address))
            table.setItem(row, 6, QTableWidgetItem(student.phone))
            table.setItem(row, 7, QTableWidgetItem(student.email))
            table.setItem(row, 8, QTableWidgetItem(student.register_date.toString("dd/MM/yyyy")))

    
    def load_students(self):
        students = self.repo.get_students_by_class(self.class_code)
        self.fill_table(students)
  

    def search_student(self):

        keyword = self.ui.txtSearch.text().strip()

        if not keyword:
            self.load_students()
            return

        students = self.repo.search_students(self.class_code, keyword)
        self.fill_table(students)



    def enable_editing(self):

        table = self.ui.dshv
        row = table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học viên")
            return

        self.editing_row = row

        table.setEditTriggers(
            table.EditTrigger.DoubleClicked |
            table.EditTrigger.SelectedClicked
        )

        self.lock_columns(row)
        self.highlight_row(row)

        QMessageBox.information(self, "Chế độ sửa", "Bạn có thể chỉnh sửa")

    

    def lock_columns(self, row):

        table = self.ui.dshv

        for col in [0, 1]:  # STT + ID
            item = table.item(row, col)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

    

    def highlight_row(self, row):

        table = self.ui.dshv

        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(Qt.GlobalColor.yellow)

   

    def save_edit(self):

        if not hasattr(self, "editing_row"):
            QMessageBox.warning(self, "Lỗi", "Chưa chọn dòng để sửa")
            return

        row = self.editing_row
        table = self.ui.dshv

        try:
            student_id = table.item(row, 1).text()
            name = table.item(row, 2).text()
            phone = table.item(row, 6).text()
            email = table.item(row, 7).text()

        except AttributeError:
            QMessageBox.warning(self, "Lỗi", "Dữ liệu không hợp lệ")
            return

        valid, message = DSHocVienBLL.validate_student(name, phone, email)

        if not valid:
            QMessageBox.warning(self, "Lỗi", message)
            return

        updated = self.repo.update_student(student_id, name, phone, email)

        if updated:
            QMessageBox.information(self, "OK", "Đã cập nhật học viên")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy học viên")

        table.setEditTriggers(table.EditTrigger.NoEditTriggers)

        del self.editing_row

        self.load_students()