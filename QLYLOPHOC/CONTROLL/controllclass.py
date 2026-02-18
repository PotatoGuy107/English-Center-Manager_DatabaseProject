
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem

from gdien.quanlyhocvien import Ui_Dialog
from BILL.class_bll import ClassBLL
from DAL.class_dal import FakeClassRepository
from MODELS.ScheduleModel import ScheduleModel
from CONTROLL.dslopp_controller import DanhSachLopController


class TaoLopController(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.repo = FakeClassRepository()

        self.class_counter = 1
        self.generate_class_code()

        self.connect_signals()
        self.init_table()
        self.load_fake_schedule()

    # --------------------------------------------------

    def generate_class_code(self):
        self.current_class_code = f"L{self.class_counter:03}"

    # --------------------------------------------------

    def connect_signals(self):
        self.ui.save.clicked.connect(self.save_class)
        self.ui.save_2.clicked.connect(self.add_schedule)
        self.ui.Button_dslop.clicked.connect(self.open_dslop)

    # --------------------------------------------------

    def open_dslop(self):
        self.dslop_window = DanhSachLopController()
        self.dslop_window.show()
        self.close()

    # --------------------------------------------------

    def init_table(self):
        self.ui.qlytrunglich_2.setRowCount(0)

    # --------------------------------------------------

    def load_fake_schedule(self):

        schedules = self.repo.get_schedules()

        for schedule in schedules:
            self.add_schedule_to_table(schedule)

    # --------------------------------------------------

    def add_schedule(self):

        class_code = self.current_class_code
        teacher = self.ui.gvphutrach_2.currentText().strip()

        raw_inputs = [
            (self.ui.dateca1_2, self.ui.ca1_2, self.ui.room1_2),
            (self.ui.dateca2_2, self.ui.ca2_2, self.ui.room1_3),
        ]

        new_schedules = []

        for date_edit, ca_box, room_box in raw_inputs:

            schedule = ScheduleModel(
                class_code,
                date_edit.date(),   
                ca_box.currentText().strip(),
                room_box.currentText().strip(),
                teacher
            )

            new_schedules.append(schedule)

        existing_schedules = self.repo.get_schedules()

        valid_rows, conflicts = ClassBLL.process_schedules(
            existing_schedules,
            new_schedules
        )

        added = False

        for schedule in valid_rows:
            self.repo.insert_schedule(schedule)
            self.add_schedule_to_table(schedule)
            added = True

        if conflicts:
            QMessageBox.warning(self, "Xung đột lịch", "\n".join(conflicts))

        if added:
            QMessageBox.information(self, "OK", "Đã thêm lịch hợp lệ")

    # --------------------------------------------------

    def add_schedule_to_table(self, schedule):

        table = self.ui.qlytrunglich_2
        row = table.rowCount()
        table.insertRow(row)

        table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        table.setItem(row, 1, QTableWidgetItem(schedule.class_code))
        table.setItem(row, 2, QTableWidgetItem(schedule.date.toString("dd/MM/yyyy")))
        table.setItem(row, 3, QTableWidgetItem(schedule.ca))
        table.setItem(row, 4, QTableWidgetItem(schedule.room))
        table.setItem(row, 5, QTableWidgetItem(schedule.teacher))
        table.setItem(row, 6, QTableWidgetItem("Hợp lệ"))

    # --------------------------------------------------

    def refresh_stt(self):
        table = self.ui.qlytrunglich_2
        for row in range(table.rowCount()):
            table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

    # --------------------------------------------------

    def save_class(self):

        data = {
            "name": self.ui.nameclass_2.text().strip(),
            "course_index": self.ui.choosecourse_2.currentIndex(),
            "skill_index": self.ui.chooseskill_2.currentIndex(),
            "teacher_index": self.ui.gvphutrach_2.currentIndex(),
            "start_date": self.ui.datestart_2.date(),
            "end_date": self.ui.dateEnd_2.date(),
            "max_class": self.ui.max_class_2.text().strip()
        }

        valid, message = ClassBLL.validate_class_info(data)

        if not valid:
            QMessageBox.warning(self, "Thiếu thông tin", message)
            self.ui.tabWidget_2.setCurrentIndex(0)
            return

        if self.repo.count_schedules_by_class(self.current_class_code) == 0:
            QMessageBox.warning(self, "Thiếu lịch học", "Bạn chưa thêm lịch học")
            self.ui.tabWidget_2.setCurrentIndex(1)
            return

        QMessageBox.information(self, "Thành công", "Lưu dữ liệu thành công!")

        self.class_counter += 1
        self.generate_class_code()
        self.ui.nameclass_2.clear()
