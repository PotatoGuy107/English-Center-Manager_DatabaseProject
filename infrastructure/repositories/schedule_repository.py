"""Repository for Schedule table operations."""
import pyodbc
from infrastructure.config.database import get_connection
from datetime import date, time


class ScheduleRepository:
    """Repository for Schedule CRUD operations."""

    @staticmethod
    def get_all() -> list:
        """Get all schedules with joined data."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.schedule_id, s.class_id, c.class_name, s.room_id, r.room_name,
                   t.full_name as teacher_name, c.max_student,
                   s.study_date, s.time_slot, s.start_time, s.end_time, c.status
            FROM Schedule s
            JOIN Class c ON s.class_id = c.class_id
            JOIN Room r ON s.room_id = r.room_id
            JOIN Teacher t ON c.teacher_id = t.teacher_id
            ORDER BY s.study_date, s.start_time
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_class(class_id: int) -> list:
        """Get all schedules for a specific class."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.schedule_id, s.class_id, c.class_name, s.room_id, r.room_name,
                   t.full_name as teacher_name, c.max_student,
                   s.study_date, s.time_slot, s.start_time, s.end_time, c.status
            FROM Schedule s
            JOIN Class c ON s.class_id = c.class_id
            JOIN Room r ON s.room_id = r.room_id
            JOIN Teacher t ON c.teacher_id = t.teacher_id
            WHERE s.class_id = ?
            ORDER BY s.study_date, s.start_time
        """, (class_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(schedule_id: int) -> tuple:
        """Get a specific schedule by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.schedule_id, s.class_id, s.room_id, s.study_date, 
                   s.time_slot, s.start_time, s.end_time
            FROM Schedule s
            WHERE s.schedule_id = ?
        """, (schedule_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert(class_id: int, room_id: int, study_date: date, 
               time_slot: str, start_time: time, end_time: time) -> tuple:
        """
        Insert a new schedule.
        Returns (success: bool, schedule_id or error_message: int|str)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Schedule (class_id, room_id, study_date, time_slot, start_time, end_time)
                OUTPUT INSERTED.schedule_id
                VALUES (?, ?, ?, ?, ?, ?)
            """, (class_id, room_id, study_date, time_slot, start_time, end_time))
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return True, new_id
        except pyodbc.IntegrityError as e:
            return False, f"Lỗi ràng buộc: {str(e)}"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def insert_batch(schedules: list) -> tuple:
        """
        Insert multiple schedules.
        schedules: list of (class_id, room_id, study_date, time_slot, start_time, end_time)
        Returns (success: bool, count or error_message: int|str)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            count = 0
            for schedule in schedules:
                cursor.execute("""
                    INSERT INTO Schedule (class_id, room_id, study_date, time_slot, start_time, end_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, schedule)
                count += 1
            conn.commit()
            conn.close()
            return True, count
        except pyodbc.IntegrityError as e:
            return False, f"Lỗi ràng buộc: {str(e)}"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def update(schedule_id: int, room_id: int, study_date: date,
               time_slot: str, start_time: time, end_time: time) -> tuple:
        """Update a schedule. Returns (success, message)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Schedule
                SET room_id = ?, study_date = ?, time_slot = ?, start_time = ?, end_time = ?
                WHERE schedule_id = ?
            """, (room_id, study_date, time_slot, start_time, end_time, schedule_id))
            conn.commit()
            conn.close()
            return True, "Cập nhật thành công"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def delete(schedule_id: int) -> tuple:
        """Delete a schedule by ID. Returns (success, message)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Schedule WHERE schedule_id = ?", (schedule_id,))
            conn.commit()
            conn.close()
            return True, "Xóa thành công"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def delete_by_class(class_id: int) -> tuple:
        """Delete all schedules for a class. Returns (success, message)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Schedule WHERE class_id = ?", (class_id,))
            conn.commit()
            conn.close()
            return True, "Xóa tất cả lịch thành công"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def check_room_conflict(room_id: int, study_date: date, 
                            start_time: time, end_time: time,
                            exclude_schedule_id: int = None) -> tuple:
        """
        Check if room is already booked at the given time.
        Returns (has_conflict: bool, conflicting_class_name or None)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT c.class_name
            FROM Schedule s
            JOIN Class c ON s.class_id = c.class_id
            WHERE s.room_id = ? 
              AND s.study_date = ?
              AND (
                  (s.start_time <= ? AND s.end_time > ?) OR
                  (s.start_time < ? AND s.end_time >= ?) OR
                  (s.start_time >= ? AND s.end_time <= ?)
              )
        """
        params = [room_id, study_date, start_time, start_time, end_time, end_time, start_time, end_time]
        
        if exclude_schedule_id:
            query += " AND s.schedule_id != ?"
            params.append(exclude_schedule_id)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, result[0]
        return False, None

    @staticmethod
    def check_teacher_conflict(class_id: int, study_date: date,
                               start_time: time, end_time: time,
                               exclude_schedule_id: int = None) -> tuple:
        """
        Check if teacher of the class is already teaching at the given time.
        Returns (has_conflict: bool, conflicting_class_name or None)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get teacher_id for this class
        cursor.execute("SELECT teacher_id FROM Class WHERE class_id = ?", (class_id,))
        teacher_row = cursor.fetchone()
        if not teacher_row:
            conn.close()
            return False, None
        teacher_id = teacher_row[0]
        
        query = """
            SELECT c.class_name
            FROM Schedule s
            JOIN Class c ON s.class_id = c.class_id
            WHERE c.teacher_id = ?
              AND s.study_date = ?
              AND s.class_id != ?
              AND (
                  (s.start_time <= ? AND s.end_time > ?) OR
                  (s.start_time < ? AND s.end_time >= ?) OR
                  (s.start_time >= ? AND s.end_time <= ?)
              )
        """
        params = [teacher_id, study_date, class_id, start_time, start_time, end_time, end_time, start_time, end_time]
        
        if exclude_schedule_id:
            query = query.replace("AND s.class_id != ?", "AND s.class_id != ? AND s.schedule_id != ?")
            params.insert(3, exclude_schedule_id)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, result[0]
        return False, None

    @staticmethod
    def get_available_rooms(study_date: date, start_time: time, end_time: time) -> list:
        """Get list of rooms that are available at the given time."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.room_id, r.room_name, r.capacity, r.location
            FROM Room r
            WHERE r.status = 'available'
              AND r.room_id NOT IN (
                  SELECT s.room_id
                  FROM Schedule s
                  WHERE s.study_date = ?
                    AND (
                        (s.start_time <= ? AND s.end_time > ?) OR
                        (s.start_time < ? AND s.end_time >= ?) OR
                        (s.start_time >= ? AND s.end_time <= ?)
                    )
              )
            ORDER BY r.room_name
        """, (study_date, start_time, start_time, end_time, end_time, start_time, end_time))
        data = cursor.fetchall()
        conn.close()
        return data
