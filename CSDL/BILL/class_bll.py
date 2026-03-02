

from DAL.class_dal import ClassDAL
from MODELS.ClassModel import ClassModel


class ClassBLL:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.dal = ClassDAL()
            cls._instance.temp_schedules = [] # Danh sách này giờ sẽ được giữ lại
        return cls._instance
 

    # ======================================================
    # LOGIC SINH MÃ LỚP HỌC (Nghiệp vụ nằm ở BLL)
    # ======================================================
    def generate_new_class_code(self):
        """Lấy mã cuối cùng từ DAL và tính toán mã mới"""
        last_code = self.dal.get_last_class_code()
        if not last_code:
            return "L001"
        
        try:
            # Tách chữ 'L' và cộng thêm 1
            num_part = int(last_code.replace("L", ""))
            return f"L{num_part + 1:03d}"
        except:
            return "L001"
    # ======================================================
    # VALIDATE CLASS
    # ======================================================

    def validate_class_info(self, data):

        if data["name"] == "":
            return False, "Tên lớp không được để trống"

        if data["end_date"] <= data["start_date"]:
            return False, "Ngày kết thúc phải sau ngày bắt đầu"

        max_class = data["max_class"]

        if max_class == "":
            return False, "Vui lòng nhập sĩ số tối đa"

        if not max_class.isdigit():
            return False, "Sĩ số tối đa phải là số"

        if int(max_class) <= 0:
            return False, "Sĩ số tối đa phải > 0"

        return True, ""

    # ======================================================
    # TẠO LỚP
    # ======================================================

    def create_class(self, data):

        valid, message = self.validate_class_info(data)
        if not valid:
            return False, message

    

        # Sinh mã ID mới (Logic BLL)
        new_class_code = self.generate_new_class_code()
        # Tạo đối tượng Model để gửi xuống DAL
        class_model = ClassModel(
            new_class_code,
            
            data["name"],
            data["course"],
            data["skill"],
            data["teacher"],
            data["start_date"],
            data["end_date"],
            int(data["max_class"]),
            progress=f"0/{data['max_class']}",
            status="Sắp khai giảng"
        )

        # Gọi DAL để lưu Class
        success, msg = self.dal.insert_class(class_model)

        if success:
            # Cập nhật mã lớp cho các lịch học tạm và lưu vào DAL
            for schedule in self.temp_schedules:
                schedule.class_code = new_class_code
            
            self.dal.insert_schedules(self.temp_schedules)
            
            # Xóa danh sách tạm sau khi lưu thành công
            self.temp_schedules.clear()
            return True, new_class_code
        
        return False, msg
    def remove_schedule(self, weekday_text, ca):
        def extract_weekday(text):
            # Tách "Thứ 2" từ "Thứ 2 (26/02/2026 - ...)"
            return text.split("(")[0].strip().lower()

        target_weekday = extract_weekday(weekday_text)
        target_ca = ca.strip().lower()

        initial_len = len(self.temp_schedules)
        self.temp_schedules = [
            s for s in self.temp_schedules
            if not (s.weekday.strip().lower() == target_weekday 
                    and s.ca.strip().lower() == target_ca)
        ]
        return len(self.temp_schedules) < initial_len

        

    # ======================================================
    # XỬ LÝ LỊCH HỌC
    # ======================================================

    def add_new_schedules(self, new_schedules_list):
        """Xử lý check trùng và thêm vào danh sách tạm"""
        # Lấy toàn bộ lịch đã có trong DB + lịch đang chờ lưu
        existing_all = self.dal.get_all_schedules() + self.temp_schedules

        valid_rows, conflicts = self.process_schedules(
            existing_all,
            new_schedules_list
        )

        # Lưu các lịch hợp lệ vào bộ nhớ tạm
        for s in valid_rows:
            self.temp_schedules.append(s)

        return valid_rows, conflicts

    def normalize(self, text):
        return str(text).strip().lower()

    def is_time_overlap(self, s1, e1, s2, e2):
        return not (e1 < s2 or e2 < s1)

    def is_duplicate_schedule(self, existing_rows, schedule):
        for row in existing_rows:
            # 1. Check khoảng thời gian ngày (Date overlap)
            overlap = self.is_time_overlap(
                row.start_date, row.end_date,
                schedule.start_date, schedule.end_date
            )
            if not overlap: continue

            # 2. Check cùng thứ (Weekday)
            if self.normalize(row.weekday) != self.normalize(schedule.weekday):
                continue

            # 3. Check cùng ca (Shift)
            if self.normalize(row.ca) != self.normalize(schedule.ca):
                continue

            # 4. Check trùng phòng hoặc trùng giảng viên
            same_room = self.normalize(row.room) == self.normalize(schedule.room)
            same_teacher = self.normalize(row.teacher) == self.normalize(schedule.teacher)

            if same_room:
                return True, f"Trùng phòng ({schedule.room})"
            if same_teacher:
                return True, f"Trùng giảng viên ({schedule.teacher})"

        return False, ""

    def process_schedules(self, existing_rows, new_schedules):
        valid_rows = []
        conflicts = []
        temp_pool = list(existing_rows)

        for schedule in new_schedules:
            if not schedule.ca or not schedule.room:
                conflicts.append(f"{schedule.weekday}: Thiếu ca hoặc phòng")
                continue

            conflict, reason = self.is_duplicate_schedule(temp_pool, schedule)

            if conflict:
                conflicts.append(f"{schedule.weekday} ({schedule.ca}): {reason}")
                continue

            valid_rows.append(schedule)
            temp_pool.append(schedule)

        return valid_rows, conflicts