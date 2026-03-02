from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate,pyqtSignal
from gdien.quanlyhocvien import Ui_Dialog
from BILL.class_bll import ClassBLL
from MODELS.ScheduleModel import ScheduleModel
from CONTROLL.dslopp_controller import DanhSachLopController

class TaoLopController(QDialog):
    logout_requested = pyqtSignal()
    def __init__(self, parent =None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tabWidget_2.setCurrentIndex(0)

        self.class_bll = ClassBLL()

        self.connect_signals()
        self.init_table()

    def connect_signals(self):
        self.ui.save.clicked.connect(self.save_class)
        self.ui.save_2.clicked.connect(self.add_schedule)
        self.ui.Button_dslop.clicked.connect(self.open_dslop)
        self.ui.delete_2.clicked.connect(self.delete_schedule)
       
        self.ui.Button_logout.clicked.connect(self.logout)

    def logout(self):
        self.logout_requested.emit()

    def open_dslop(self):
        self.dslop_window = DanhSachLopController()
        self.dslop_window.load_data()
        self.dslop_window.show()
        self.close()

    # Trong controllclass.py

    def init_table(self):
        table = self.ui.qlytrunglich_2
        table.setRowCount(0)
        
        # 1. Hiển thị lại các lớp đã lưu chính thức từ DAL
        all_classes = self.class_bll.dal.get_all_classes()
        for cls in all_classes:
            schedules = self.class_bll.dal.get_schedules_by_class(cls.code)
            for s in schedules:
                self.add_schedule_to_table(s, "Đã lưu")

        # 2. HIỂN THỊ LẠI CÁC LỊCH ĐANG TẠO DỞ (Quan trọng nhất)
        # Nhờ Singleton ở BLL, danh sách này sẽ không bị mất khi bạn quay lại
        for s in self.class_bll.temp_schedules:
            self.add_schedule_to_table(s, "Hợp lệ")

    def add_schedule(self):
        teacher = self.ui.gvphutrach_2.currentText().strip()
        raw_inputs = [
            (self.ui.dateca1_2, self.ui.ca1_2, self.ui.room1_2),
            (self.ui.dateca2_2, self.ui.ca2_2, self.ui.room1_3),
        ]

        new_schedules = []
        for date_edit, ca_box, room_box in raw_inputs:
            start_date = self.ui.datestart_2.date()
            end_date = self.ui.dateEnd_2.date()
            weekday = date_edit.date().toString("dddd")

            # Việt hóa thứ
            dic_weekday = {
                "Monday": "Thứ 2", "Tuesday": "Thứ 3", "Wednesday": "Thứ 4",
                "Thursday": "Thứ 5", "Friday": "Thứ 6", "Saturday": "Thứ 7", "Sunday": "Chủ nhật"
            }
            for eng, vie in dic_weekday.items():
                weekday = weekday.replace(eng, vie)

            schedule = ScheduleModel(
                None, start_date, end_date, weekday,
                ca_box.currentText().strip(),
                room_box.currentText().strip(),
                teacher
            )
            new_schedules.append(schedule)

        valid_rows, conflicts = self.class_bll.add_new_schedules(new_schedules)

        for schedule in valid_rows:
            self.add_schedule_to_table(schedule, "Hợp lệ")

        if conflicts:
            QMessageBox.warning(self, "Xung đột lịch", "\n".join(conflicts))
        if valid_rows:
            QMessageBox.information(self, "OK", "Đã thêm lịch thành công")

    def add_schedule_to_table(self, schedule, status):
        table = self.ui.qlytrunglich_2
        row = table.rowCount()
        table.insertRow(row)

        # Cột 0: STT
        table.setItem(row, 0, QTableWidgetItem(str(row + 1))) 
        
        # Cột 1: Mã lớp (Lấy từ Model, nếu None thì hiển thị "Chờ lưu")
        class_code = schedule.class_code if schedule.class_code else "Chờ lưu..."
        table.setItem(row, 1, QTableWidgetItem(class_code)) 

        # Cột 2: Giảng viên
        table.setItem(row, 2, QTableWidgetItem(schedule.teacher)) 
        
        # Cột 3: Sĩ số (Khi có SQL, giá trị này sẽ lấy từ thuộc tính của lớp học)
        # Tạm thời hiển thị "0/Max"
        max_val = self.ui.max_class_2.text() or "0"
        table.setItem(row, 3, QTableWidgetItem(f"0/{max_val}")) 

        # Cột 4: Ngày (Thứ + Khoảng thời gian)
        time_info = f"{schedule.weekday} ({schedule.start_date.toString('dd/MM/yyyy')} - {schedule.end_date.toString('dd/MM/yyyy')})"
        table.setItem(row, 4, QTableWidgetItem(time_info))

        # Cột 5: Ca
        table.setItem(row, 5, QTableWidgetItem(schedule.ca))
        
        # Cột 6: Phòng
        table.setItem(row, 6, QTableWidgetItem(schedule.room))
        
        # Cột 7: Trạng thái
        table.setItem(row, 7, QTableWidgetItem(status))

    def delete_schedule(self):
        table = self.ui.qlytrunglich_2
        selected_row = table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lịch cần xóa")
            return

        weekday_item = table.item(selected_row, 4)  # Cột Ngày
        ca_item = table.item(selected_row, 5)       # Cột Ca

        if not weekday_item or not ca_item:
            QMessageBox.warning(self, "Lỗi", "Không đọc được dữ liệu lịch")
            return

        weekday_text = weekday_item.text()
        ca = ca_item.text()

        removed = self.class_bll.remove_schedule(weekday_text, ca)

        if removed:
            table.removeRow(selected_row)
            self.refresh_stt()
            QMessageBox.information(self, "Thành công", "Đã xóa lịch học")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy lịch trong danh sách tạm")

    def refresh_stt(self):
        table = self.ui.qlytrunglich_2
        for row in range(table.rowCount()):
            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

    def save_class(self):
        data = {
            "name": self.ui.nameclass_2.text().strip(),
            "course": self.ui.choosecourse_2.currentText(),
            "skill": self.ui.chooseskill_2.currentText(),
            "teacher": self.ui.gvphutrach_2.currentText(),
            "start_date": self.ui.datestart_2.date(),
            "end_date": self.ui.dateEnd_2.date(),
            "max_class": self.ui.max_class_2.text().strip()
        }

        success, result = self.class_bll.create_class(data)

        if success:
            new_class_code = result   # ⚠️ BLL phải return class_code

            table = self.ui.qlytrunglich_2

            for row in range(table.rowCount()):
                item = table.item(row, 1)
                if item and item.text() == "Chờ lưu...":
                    table.setItem(row, 1, QTableWidgetItem(new_class_code))
                    table.setItem(row, 7, QTableWidgetItem("Đã lưu"))

            QMessageBox.information(
                self,
                "Thành công",
                f"Lưu lớp {new_class_code} thành công!"
            )

            self.clear_input_fields()

        else:
            QMessageBox.warning(self, "Lỗi", result)

    def clear_input_fields(self):
        """Chỉ xóa nội dung các ô nhập, giữ nguyên bảng dữ liệu"""
        self.ui.nameclass_2.clear()
        self.ui.max_class_2.clear()
        self.ui.choosecourse_2.setCurrentIndex(0)
        self.ui.chooseskill_2.setCurrentIndex(0)
        self.ui.gvphutrach_2.setCurrentIndex(0)

        today = QDate.currentDate()
        self.ui.datestart_2.setDate(today)
        self.ui.dateEnd_2.setDate(today)
 
    def reset_form(self):
        self.ui.nameclass_2.clear()
        self.ui.max_class_2.clear()
        self.ui.qlytrunglich_2.setRowCount(0)
        self.class_bll.temp_schedules.clear()

    