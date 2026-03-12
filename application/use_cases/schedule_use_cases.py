"""Use cases for Schedule management."""
from datetime import date, time, timedelta
from typing import List, Tuple
from infrastructure.repositories.schedule_repository import ScheduleRepository


class ScheduleUseCases:
    """Business logic for schedule operations."""

    # Time slot definitions
    TIME_SLOTS = {
        "Ca 1 (07:00 - 10:00)": ("07:00", "10:00"),
        "Ca 2 (10:00 - 12:30)": ("10:00", "12:30"),
        "Ca 3 (13:30 - 16:00)": ("13:30", "16:00"),
        "Ca 4 (18:00 - 20:30)": ("18:00", "20:30"),
    }

    def __init__(self):
        self.repository = ScheduleRepository

    def get_all_schedules(self) -> list:
        """Get all schedules with class and room info."""
        return self.repository.get_all()

    def get_schedules_by_class(self, class_id: int) -> list:
        """Get all schedules for a specific class."""
        return self.repository.get_by_class(class_id)

    def parse_time_slot(self, time_slot_text: str) -> Tuple[time, time]:
        """Parse time slot text to start_time and end_time."""
        if time_slot_text in self.TIME_SLOTS:
            start_str, end_str = self.TIME_SLOTS[time_slot_text]
        else:
            # Default to Ca 1 if not found
            start_str, end_str = "07:00", "10:00"
        
        start_parts = start_str.split(":")
        end_parts = end_str.split(":")
        
        start_time = time(int(start_parts[0]), int(start_parts[1]))
        end_time = time(int(end_parts[0]), int(end_parts[1]))
        
        return start_time, end_time

    def add_schedule(self, class_id: int, room_id: int, 
                     study_date: date, time_slot: str) -> Tuple[bool, str]:
        """
        Add a single schedule entry.
        Returns (success, message)
        """
        if not class_id:
            return False, "Vui lòng chọn lớp học"
        if not room_id:
            return False, "Vui lòng chọn phòng học"
        if not study_date:
            return False, "Vui lòng chọn ngày học"
        if not time_slot:
            return False, "Vui lòng chọn ca học"

        # Parse time slot
        start_time, end_time = self.parse_time_slot(time_slot)

        # Check for room conflict
        has_conflict, conflict_class = self.repository.check_room_conflict(
            room_id, study_date, start_time, end_time
        )
        if has_conflict:
            return False, f"Phòng đã được sử dụng bởi lớp '{conflict_class}'"

        # Check for teacher conflict
        has_conflict, conflict_class = self.repository.check_teacher_conflict(
            class_id, study_date, start_time, end_time
        )
        if has_conflict:
            return False, f"Giảng viên đã dạy lớp '{conflict_class}' vào thời gian này"

        # Insert schedule
        success, result = self.repository.insert(
            class_id, room_id, study_date, time_slot, start_time, end_time
        )
        
        if success:
            return True, f"Đã thêm lịch học (ID: {result})"
        return False, result

    def add_recurring_schedule(self, class_id: int, room_id: int,
                               start_date: date, end_date: date,
                               weekday: int, time_slot: str) -> Tuple[bool, str]:
        """
        Add recurring schedule from start_date to end_date on specific weekday.
        weekday: 0=Monday, 6=Sunday
        Returns (success, message)
        """
        if not class_id:
            return False, "Vui lòng chọn lớp học"
        if not room_id:
            return False, "Vui lòng chọn phòng học"
        if start_date > end_date:
            return False, "Ngày bắt đầu phải trước ngày kết thúc"

        # Parse time slot
        start_time, end_time = self.parse_time_slot(time_slot)

        # Generate all dates for the weekday
        schedules_to_add = []
        conflicts = []
        current_date = start_date

        # Find first occurrence of weekday
        while current_date.weekday() != weekday:
            current_date += timedelta(days=1)
            if current_date > end_date:
                return False, "Không có ngày nào phù hợp trong khoảng thời gian"

        # Generate dates
        while current_date <= end_date:
            # Check room conflict
            has_conflict, conflict_class = self.repository.check_room_conflict(
                room_id, current_date, start_time, end_time
            )
            if has_conflict:
                conflicts.append(f"{current_date.strftime('%d/%m/%Y')} (phòng - {conflict_class})")
                current_date += timedelta(days=7)
                continue

            # Check teacher conflict
            has_conflict, conflict_class = self.repository.check_teacher_conflict(
                class_id, current_date, start_time, end_time
            )
            if has_conflict:
                conflicts.append(f"{current_date.strftime('%d/%m/%Y')} (GV - {conflict_class})")
                current_date += timedelta(days=7)
                continue

            schedules_to_add.append((
                class_id, room_id, current_date, time_slot, start_time, end_time
            ))
            current_date += timedelta(days=7)

        if not schedules_to_add:
            if conflicts:
                return False, f"Tất cả ngày đều xung đột: {', '.join(conflicts[:3])}..."
            return False, "Không có lịch nào được tạo"

        # Insert all schedules
        success, result = self.repository.insert_batch(schedules_to_add)
        
        if success:
            msg = f"Đã thêm {result} buổi học"
            if conflicts:
                msg += f"\nBỏ qua {len(conflicts)} ngày xung đột"
            return True, msg
        return False, result

    def delete_schedule(self, schedule_id: int) -> Tuple[bool, str]:
        """Delete a specific schedule."""
        if not schedule_id:
            return False, "Vui lòng chọn lịch cần xóa"
        return self.repository.delete(schedule_id)

    def delete_all_schedules_for_class(self, class_id: int) -> Tuple[bool, str]:
        """Delete all schedules for a class."""
        if not class_id:
            return False, "Vui lòng chọn lớp học"
        return self.repository.delete_by_class(class_id)

    def get_available_rooms(self, study_date: date, time_slot: str) -> list:
        """Get rooms available for a specific date and time slot."""
        start_time, end_time = self.parse_time_slot(time_slot)
        return self.repository.get_available_rooms(study_date, start_time, end_time)

    def format_schedule_for_display(self, schedule_data: tuple) -> dict:
        """
        Format schedule tuple for display.
        Input: (schedule_id, class_id, class_name, room_id, room_name, 
                teacher_name, max_student, study_date, time_slot, start_time, end_time, status)
        """
        return {
            "schedule_id": schedule_data[0],
            "class_id": schedule_data[1],
            "class_name": schedule_data[2],
            "room_id": schedule_data[3],
            "room_name": schedule_data[4],
            "teacher_name": schedule_data[5],
            "max_student": schedule_data[6],
            "study_date": schedule_data[7],
            "time_slot": schedule_data[8],
            "start_time": schedule_data[9],
            "end_time": schedule_data[10],
            "status": schedule_data[11]
        }
