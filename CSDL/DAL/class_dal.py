

from MODELS.ScheduleModel import ScheduleModel
from MODELS.ClassModel import ClassModel
from PyQt6.QtCore import QDate

class ClassDAL:
    _instance = None
    

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Khởi tạo danh sách nếu chưa có
            if not hasattr(cls._instance, 'classes'):
                cls._instance.classes = [
                    ClassModel("L001", "Speaking", "Basic Course", "Speaking", "GV A", 
                               QDate(2026, 1, 1), QDate(2026, 2, 28), 25)
                ]
            if not hasattr(cls._instance, 'schedules'):
                cls._instance.schedules = []
        return cls._instance

    # CLASS QUERIES (Truy vấn lớp học)
 
    
    def get_all_classes(self):
        """Trả về danh sách tất cả các lớp"""
        return self.classes

    def get_last_class_code(self):
        """Chỉ làm nhiệm vụ lấy mã cuối cùng, không tính toán mã mới"""
        if not self.classes:
            return None
        # Giả sử danh sách đã được sắp xếp, lấy mã cuối cùng
        return self.classes[-1].code

    def insert_class(self, class_obj):
        """Chỉ thực hiện lệnh chèn dữ liệu"""
        try:
            self.classes.append(class_obj)
            return True, class_obj.code
        except Exception as e:
            return False, f"Lỗi DAL: {str(e)}"

    # SCHEDULE QUERIES (Truy vấn lịch học)
  

    def get_all_schedules(self):
        return self.schedules

    def insert_schedules(self, schedule_list):
        """Lưu danh sách lịch học"""
        try:
            self.schedules.extend(schedule_list)
            return True
        except:
            return False

    def get_schedules_by_class(self, class_code):
        return [s for s in self.schedules if s.class_code == class_code]
    
    def delete_schedule_item(self, class_code, weekday, ca):
        weekday = weekday.strip().lower()
        ca = ca.strip().lower()

        self.schedules = [
            s for s in self.schedules
            if not (
                s.class_code == class_code
                and s.weekday.strip().lower() == weekday
                and s.ca.strip().lower() == ca
            )
        ]
        return True