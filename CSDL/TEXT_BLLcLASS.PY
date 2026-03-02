
"""from MODELS.ScheduleModel import ScheduleModel
from MODELS.ClassModel import ClassModel
from PyQt6.QtCore import QDate


class FakeDATARepository:
    _instance = None
    classes = []
    schedules = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Khởi tạo dữ liệu mẫu (Sau này thay bằng kết nối SQL Server)
            cls._instance.classes = [
                ClassModel(
                    "L001",
                    "Speaking",
                    "Basic Course",
                    "Speaking",      
                    "GV A",
                    QDate(2026, 1, 1),
                    QDate(2026, 2, 28),
                    25
                )
            ]


          
            cls._instance.schedules = [
                ScheduleModel(
                    "L001",
                    QDate(2026, 1, 1),
                    QDate(2026, 2, 28),
                    "Thứ 2",
                    "Ca 1",
                    "101",
                    "GV A"
                )
            ]

        return cls._instance
           

    

    #Class Crud
    def get_all_classes(self):
        return self.classes

    
    def add_class(self, class_data):
        self.classes.append(class_data)
        
    def generate_class_code(self):
        max_id = 0

        for c in self.classes:
            try:
                num = int(c.code.replace("L", ""))
                max_id = max(max_id, num)
            except:
                pass


        return f"L{max_id + 1:03d}"
    #Schedule Crud
    def add_schedule(self, schedule):
        self.insert_schedule(schedule)

    def insert_schedule(self, schedule):
        self.schedules.append(schedule)


    def get_schedules(self):
        return self.schedules
    
    
    def get_schedules_by_class(self, class_code):
        return [
            s for s in self.schedules
            if s.class_code == class_code
        ]

    def count_schedules_by_class(self, class_code):
        return sum(1 for s in self.schedules if s.class_code == class_code)
    
    def delete_schedule(self, class_code, weekday_text, ca):
        def extract_weekday(text):
            return text.split("(")[0].strip().lower()

        target_weekday = extract_weekday(weekday_text)

        self.schedules = [
            s for s in self.schedules
            if not (
                s.class_code == class_code
                and s.weekday.strip().lower() == target_weekday
                and s.ca == ca
            )
        ]
    def delete_schedules_by_class(self, class_code):
        self.schedules = [
            s for s in self.schedules
            if s.class_code != class_code
        ]

    """
"""
from gdien.dslopp import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem

from DAL.class_dal import ClassDAL


from CONTROLL.dshocvien_controller import DanhSachHocVienController
from CONTROLL.taokythi_controll import TaoKyThiController




class DanhSachLopController(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.selected_class_code = None 
        self.dshv_window = None
        self.repo = ClassDAL()
        self.connect_signals()
        self.load_data()

    



    def connect_signals(self):
        self.ui.return_2.clicked.connect(self.go_back)
        self.ui.taokythi.clicked.connect(self.open_taokythi)
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

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()
        


    
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

    def open_taokythi(self):
        if not self.selected_class_code:
            QMessageBox.warning(
                self,
                "Chưa chọn lớp",
                "Vui lòng chọn lớp trước khi tạo kỳ thi"
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



    def load_data(self):
        repo = ClassDAL()
        data = repo.get_all_classes()

        table = self.ui.dslopqli
        table.setRowCount(0)

        for c in data:  # c = ClassModel
            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, tableItem(str(row + 1)))  
            table.setItem(row, 1, tableItem(c.code))
            table.setItem(row, 2, tableItem(c.name))
            table.setItem(row, 3, tableItem(c.course))
            table.setItem(row, 4, tableItem(c.teacher))
            table.setItem(row, 5, tableItem(
                f"{c.start_date} - {c.end_date}"
            ))
            table.setItem(row, 6, tableItem(c.progress))
            table.setItem(row, 7, tableItem(c.status))    
                


def tableItem(text):
    return QTableWidgetItem(text)
"""
"""test dsvh_dal
from MODELS.student import Student
from PyQt6.QtCore import QDate


class FakeStudentRepository:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
                
            cls._instance.students = [

                Student(
                    "L001",                
                    "HV001",               
                    "Nguyễn Văn An",      
                    QDate(2005, 5, 12),     
                    "Nam",
                    "Hà Nội",
                    "0912345678",
                    "an@gmail.com",
                    QDate(2026, 1, 10)   
                ),

                Student(
                    "L001",
                    "HV002",
                    "Trần Thị Bình",
                    QDate(2004, 8, 25),
                    "Nữ",
                    "Đà Nẵng",
                    "0987654321",
                    "binh@gmail.com",
                    QDate(2026, 1, 15)
                ),
                Student (
                        "L002",
                        "HV003",
                        "Lê Văn C",
                        QDate(2006, 1, 5),
                        "Nam",
                        "TP.HCM",
                        "0909123456",
                        "c@gmail.com",
                        QDate.currentDate()
                    ),
            ]
            cls._instance.next_id = 4
        
        return cls._instance
    
    

    def get_students_by_class(self, class_code):
        return [
            s for s in self.students
            if s.class_code == class_code
        ]


    def search_students(self, keyword):

        keyword = keyword.strip().lower()


        return [
            s for s in self.students
            if keyword in s.student_id.lower()
            or keyword in s.name.lower()
        ]
    def update_student(self, student_id, name, phone, email):

            for s in self.students:
                if s.student_id == student_id:
                    s.name = name
                    s.phone = phone
                    s.email = email
                    return True

            return False
    #id dùng tạm lúc chưa tích hợp sql
    def add_student(self, student):
        self.students.append(student)
        self.next_id += 1
        
    def generate_student_id(self):
        max_id = 0

        for s in self.students:
            try:
                num = int(s.student_id.replace("HV", ""))
                if num > max_id:
                    max_id = num
            except:
                pass

        return f"HV{max_id + 1:03d}"
    def exists(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return True
        return False
    def delete_student(self, student_id):
        self.students = [
            s for s in self.students
            if s.student_id != student_id
        ]

"""