class ClassBLL:

    @staticmethod
    def validate_class_info(data):

        if data["name"] == "":
            return False, "Tên lớp không được để trống"

        if data["course_index"] == 0:
            return False, "Vui lòng chọn khóa học"

        if data["skill_index"] == 0:
            return False, "Vui lòng chọn kỹ năng"

        if data["teacher_index"] == 0:
            return False, "Vui lòng chọn giảng viên"

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

    # --------------------------------------------

    @staticmethod
    def normalize(text):
        return text.strip().lower()

    # --------------------------------------------

    @staticmethod
    def is_duplicate_schedule(existing_rows, schedule):

        for row in existing_rows:

            same_date = row.date == schedule.date
            same_ca = ClassBLL.normalize(row.ca) == ClassBLL.normalize(schedule.ca)
            same_room = ClassBLL.normalize(row.room) == ClassBLL.normalize(schedule.room)
            same_teacher = ClassBLL.normalize(row.teacher) == ClassBLL.normalize(schedule.teacher)
            same_class = row.class_code == schedule.class_code

            if same_date and same_ca and same_room:
                return True, f"Trùng phòng ({schedule.room})"

            if same_date and same_ca and same_teacher:
                return True, f"Trùng giảng viên ({schedule.teacher})"

            if same_class and same_date and same_ca:
                return True, "Lớp đã có lịch ca này"

        return False, ""

    # --------------------------------------------

    @staticmethod
    def process_schedules(existing_rows, schedules):

        valid_rows = []
        conflicts = []

        for schedule in schedules:

            if not schedule.ca or not schedule.room:
                conflicts.append(
                    f"{schedule.date} → Thiếu ca hoặc phòng"
                )
                continue

            conflict, reason = ClassBLL.is_duplicate_schedule(
                existing_rows,
                schedule
            )

            if conflict:
                conflicts.append(
                    f"{schedule.date} - {schedule.ca} → {reason}"
                )
                continue

            valid_rows.append(schedule)

        return valid_rows, conflicts
class ClassBLL:

    @staticmethod
    def validate_class_info(data):

        if data["name"] == "":
            return False, "Tên lớp không được để trống"

        if data["course_index"] == 0:
            return False, "Vui lòng chọn khóa học"

        if data["skill_index"] == 0:
            return False, "Vui lòng chọn kỹ năng"

        if data["teacher_index"] == 0:
            return False, "Vui lòng chọn giảng viên"

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

    # --------------------------------------------

    @staticmethod
    def normalize(text):
        return text.strip().lower()

    # --------------------------------------------

    @staticmethod
    def is_duplicate_schedule(existing_rows, schedule):

        for row in existing_rows:

            same_date = row.date == schedule.date
            same_ca = ClassBLL.normalize(row.ca) == ClassBLL.normalize(schedule.ca)
            same_room = ClassBLL.normalize(row.room) == ClassBLL.normalize(schedule.room)
            same_teacher = ClassBLL.normalize(row.teacher) == ClassBLL.normalize(schedule.teacher)
            same_class = row.class_code == schedule.class_code

            if same_date and same_ca and same_room:
                return True, f"Trùng phòng ({schedule.room})"

            if same_date and same_ca and same_teacher:
                return True, f"Trùng giảng viên ({schedule.teacher})"

            if same_class and same_date and same_ca:
                return True, "Lớp đã có lịch ca này"

        return False, ""

    # --------------------------------------------

    @staticmethod
    def process_schedules(existing_rows, schedules):

        valid_rows = []
        conflicts = []

        for schedule in schedules:

            if not schedule.ca or not schedule.room:
                conflicts.append(
                    f"{schedule.date} → Thiếu ca hoặc phòng"
                )
                continue

            conflict, reason = ClassBLL.is_duplicate_schedule(
                existing_rows,
                schedule
            )

            if conflict:
                conflicts.append(
                    f"{schedule.date} - {schedule.ca} → {reason}"
                )
                continue

            valid_rows.append(schedule)

        return valid_rows, conflicts
