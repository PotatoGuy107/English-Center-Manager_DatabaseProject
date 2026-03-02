from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from gdien.nhapdiem import Ui_Dialog
from BILL.teacher.nhapdiem_bll import nhapdiemBLL

class NhapDiem(QDialog):
    def __init__(self, class_code, ky_thi):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.class_code = class_code
        self.ky_thi = ky_thi

        self.bll = nhapdiemBLL()

        self.ui.labelmalop.setText(class_code)
        self.ui.ky_thi.setText(ky_thi)

        

        # Kết nối nút
        self.ui.btnsua_2.clicked.connect(self.luu_diem)   # nút LƯU
        self.ui.btnsua.clicked.connect(self.bat_sua)      # nút SỬA
        self.ui.Button_return.clicked.connect(self.close)
        
        

        self.load_data()


    def load_data(self):
        students = self.bll.get_students_by_class(self.class_code)
        scores = self.bll.get_scores(self.class_code, self.ky_thi)

        score_dict = {s.student_id: s.diem for s in scores}

        self.ui.danhsachhocvien.setRowCount(len(students))

        for row, s in enumerate(students):
            self.ui.danhsachhocvien.setItem(row, 0, QTableWidgetItem(str(row+1)))
            self.ui.danhsachhocvien.setItem(row, 1, QTableWidgetItem(s.student_id))
            self.ui.danhsachhocvien.setItem(row, 2, QTableWidgetItem(s.name))
            self.ui.danhsachhocvien.setItem(row, 3, QTableWidgetItem(s.birth.toString("dd/MM/yyyy")))

            diem = score_dict.get(s.student_id, "")
            diem_item = QTableWidgetItem(str(diem))
            diem_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEditable |
                Qt.ItemFlag.ItemIsEnabled
            )

            self.ui.danhsachhocvien.setItem(row, 4, diem_item)
        
    def bat_sua(self):
        table = self.ui.danhsachhocvien

        current_row = table.currentRow()

        if current_row < 0:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn học viên!")
            return

        table.setEditTriggers(table.EditTrigger.AllEditTriggers)

        # Chọn đúng ô điểm của dòng đang chọn
        table.setCurrentCell(current_row, 4)
        table.editItem(table.currentItem())
    def luu_diem(self):
        row_count = self.ui.danhsachhocvien.rowCount()

        for row in range(row_count):
            student_id = self.ui.danhsachhocvien.item(row, 1).text()
            diem_item = self.ui.danhsachhocvien.item(row, 4)

            if diem_item is None:
                continue

            diem_text = diem_item.text().strip()

            if diem_text == "":
                continue

            try:
                diem = float(diem_text)
            except ValueError:
                QMessageBox.warning(self, "Lỗi", f"Điểm không hợp lệ ở dòng {row+1}")
                return

            # Gửi xuống BLL
            self.bll.save_score(
                self.class_code,
                student_id,
                self.ky_thi,
                diem
            )

        QMessageBox.information(self, "Thành công", "Lưu điểm thành công!")
        self.ui.danhsachhocvien.setEditTriggers(
            self.ui.danhsachhocvien.EditTrigger.NoEditTriggers
        )
        # Sau khi lưu xong khóa lại không cho sửa
        
    
