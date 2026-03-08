import unicodedata

from domain.entities.class_entity import Class
from domain.entities.schedule_entity import Schedule
from infrastructure.repositories.class_repository import ClassRepository


class ClassUseCases:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.repo = ClassRepository()
            cls._instance.temp_schedules = []
        return cls._instance

    def generate_new_class_code(self) -> str:
        last = self.repo.get_last_class_code()
        if not last:
            return "L001"
        try:
            num = int(last[1:])
            return f"L{num + 1:03d}"
        except ValueError:
            return "L001"

    def validate_class_info(self, data) -> tuple[bool, str]:
        if not data.get("name"):
            return False, "Class name is required"
        if not data.get("course"):
            return False, "Course is required"
        if not data.get("teacher"):
            return False, "Teacher is required"
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and start > end:
            return False, "Start date must be before end date"
        return True, ""

    def create_class(self, data) -> tuple[bool, str]:
        valid, msg = self.validate_class_info(data)
        if not valid:
            return False, msg

        code = self.generate_new_class_code()
        class_obj = Class(
            code=code,
            name=data["name"],
            course=data["course"],
            skill=data.get("skill", ""),
            teacher=data["teacher"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            max_students=int(data.get("max_students", 20)),
            status=data.get("status", "Sắp khai giảng"),
            progress=f"0/{data.get('max_students', 20)}",
        )
        success, msg = self.repo.insert_class(class_obj)
        if success and self.temp_schedules:
            for s in self.temp_schedules:
                s.class_code = code
            self.repo.insert_schedules(self.temp_schedules)
            self.temp_schedules = []
        return success, msg if not success else code

    def remove_schedule(self, weekday_text, shift) -> bool:
        self.temp_schedules = [
            s for s in self.temp_schedules
            if not (s.weekday == weekday_text and s.shift == shift)
        ]
        return True

    def add_new_schedules(self, new_schedules_list) -> tuple[list, list]:
        existing_rows = self.repo.get_all_schedules()
        return self.process_schedules(existing_rows, new_schedules_list)

    def normalize(self, text) -> str:
        return unicodedata.normalize("NFC", text.strip().lower())

    def is_time_overlap(self, s1, e1, s2, e2) -> bool:
        return s1 <= e2 and s2 <= e1

    def is_duplicate_schedule(self, existing_rows, schedule) -> tuple[bool, str]:
        for ex in existing_rows:
            if ex.class_code == schedule.class_code:
                continue
            if self.normalize(ex.weekday) != self.normalize(schedule.weekday):
                continue
            if not self.is_time_overlap(
                schedule.start_date, schedule.end_date, ex.start_date, ex.end_date
            ):
                continue
            if self.normalize(ex.shift) == self.normalize(schedule.shift):
                if self.normalize(ex.room) == self.normalize(schedule.room):
                    return True, f"Room conflict: {schedule.room}"
                if self.normalize(ex.teacher) == self.normalize(schedule.teacher):
                    return True, f"Teacher conflict: {schedule.teacher}"
        return False, ""

    def process_schedules(self, existing_rows, new_schedules) -> tuple[list, list]:
        accepted = []
        rejected = []
        for s in new_schedules:
            conflict, reason = self.is_duplicate_schedule(existing_rows + accepted, s)
            if conflict:
                rejected.append((s, reason))
            else:
                accepted.append(s)
        self.temp_schedules.extend(accepted)
        return accepted, rejected
