import unicodedata

from domain.entities.class_entity import Class
from domain.entities.schedule_entity import Schedule
from infrastructure.repositories.class_repository import ClassRepository
from infrastructure.config.database import get_connection


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
            num = int(last) if isinstance(last, int) else int(last[1:])
            return f"L{num + 1:03d}"
        except ValueError:
            return "L001"

    def _get_skill_id_by_name(self, skill_name: str) -> int:
        """Get skill_id from skill name"""
        if not skill_name:
            return 1  # Default skill
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT skill_id FROM Skill WHERE skill_name = ?", (skill_name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 1

    def _get_teacher_id_by_name(self, teacher_name: str) -> int:
        """Get teacher_id from teacher name"""
        if not teacher_name:
            return 1  # Default teacher
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id FROM Teacher WHERE full_name = ?", (teacher_name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 1

    def _format_date(self, date_obj) -> str:
        """Convert QDate or date object to SQL Server format yyyy-MM-dd"""
        if hasattr(date_obj, 'toString'):
            # QDate object
            return date_obj.toString("yyyy-MM-dd")
        elif hasattr(date_obj, 'strftime'):
            # Python date/datetime
            return date_obj.strftime("%Y-%m-%d")
        return str(date_obj)

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
        
        # Get skill_id - either passed directly as int or get from name
        skill = data.get("skill", "")
        if isinstance(skill, int):
            skill_id = skill
        elif isinstance(skill, str) and skill.isdigit():
            skill_id = int(skill)
        else:
            skill_id = self._get_skill_id_by_name(skill)
        
        # Get teacher_id - either passed directly as int or get from name
        teacher = data.get("teacher", "")
        if isinstance(teacher, int):
            teacher_id = teacher
        elif isinstance(teacher, str) and teacher.isdigit():
            teacher_id = int(teacher)
        else:
            teacher_id = self._get_teacher_id_by_name(teacher)
        
        # Format dates for SQL Server
        start_date = self._format_date(data["start_date"])
        end_date = self._format_date(data["end_date"])
        
        # Prepare tuple for insert: (class_name, skill_id, teacher_id, start_date, end_date, max_student, status)
        class_data = (
            data["name"],
            skill_id,
            teacher_id,
            start_date,
            end_date,
            int(data.get("max_students", 20)),
            data.get("status", "Active")
        )
        
        success, result = self.repo.insert_class(class_data)
        if success and self.temp_schedules:
            for s in self.temp_schedules:
                s.class_code = result  # result is the new class_id
            self.repo.insert_schedules(self.temp_schedules)
            self.temp_schedules = []
        return success, str(result)

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
