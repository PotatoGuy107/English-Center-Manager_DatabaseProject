import pyodbc
from domain.entities.class_entity import Class
from domain.entities.schedule_entity import Schedule
from domain.interfaces.i_class_repository import IClassRepository
from infrastructure.config.database import get_connection


class ClassRepository(IClassRepository):
    """Repository for Class and Schedule using SQL Server database."""

    @staticmethod
    def get_next_class_id() -> str:
        """Generate next class_id like CL01, CL02, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(class_id, 3, LEN(class_id)-2) AS INT)) FROM Class WHERE class_id LIKE 'CL%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"CL{max_num + 1:02d}"

    @staticmethod
    def get_next_schedule_id() -> str:
        """Generate next schedule_id like SC001, SC002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(schedule_id, 3, LEN(schedule_id)-2) AS INT)) FROM Schedule WHERE schedule_id LIKE 'SC%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"SC{max_num + 1:03d}"

    @staticmethod
    def get_all_classes() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.class_id, c.class_name, co.course_name, sk.skill_name, 
                   c.teacher_id, c.start_date, c.end_date, c.max_student, c.status
            FROM Class c
            LEFT JOIN Skill sk ON c.skill_id = sk.skill_id
            LEFT JOIN Course co ON sk.course_id = co.course_id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_class_by_id(class_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.class_id, c.class_name, c.skill_id, c.teacher_id, 
                   c.start_date, c.end_date, c.max_student, c.status
            FROM Class c
            WHERE c.class_id = ?
        """, (class_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_last_class_code() -> str:
        """Get the last class_id"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(class_id, 3, LEN(class_id)-2) AS INT)) FROM Class WHERE class_id LIKE 'CL%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"CL{max_num:02d}" if max_num > 0 else None

    @staticmethod
    def insert_class(class_data) -> tuple:
        """Insert class. class_data = (class_id, class_name, skill_id, teacher_id, start_date, end_date, max_student, status). Returns (success, class_id or error)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Class (class_id, class_name, skill_id, teacher_id, start_date, end_date, max_student, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, class_data)
            conn.commit()
            conn.close()
            return True, class_data[0]
        except pyodbc.IntegrityError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update_class(class_data) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Class
                SET class_name=?, skill_id=?, teacher_id=?, start_date=?, end_date=?, max_student=?, status=?
                WHERE class_id=?
            """, (class_data[1], class_data[2], class_data[3], class_data[4], 
                  class_data[5], class_data[6], class_data[7], class_data[0]))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def delete_class(class_id) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Class WHERE class_id=?", (class_id,))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_classes_by_teacher(teacher_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.class_id, c.class_name, sk.skill_name, c.start_date, c.end_date, c.status
            FROM Class c
            LEFT JOIN Skill sk ON c.skill_id = sk.skill_id
            WHERE c.teacher_id = ?
        """, (teacher_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    # ==================== SCHEDULE METHODS ====================

    @staticmethod
    def get_all_schedules() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.schedule_id, s.class_id, s.room_id, s.study_date, 
                   s.time_slot, s.start_time, s.end_time
            FROM Schedule s
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_schedules_by_class(class_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.schedule_id, r.room_name, s.study_date, s.time_slot, s.start_time, s.end_time
            FROM Schedule s
            LEFT JOIN Room r ON s.room_id = r.room_id
            WHERE s.class_id = ?
        """, (class_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_schedule(schedule_data) -> str:
        """Insert schedule. schedule_data = (schedule_id, class_id, room_id, study_date, time_slot, start_time, end_time). Returns schedule_id or None."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Schedule (schedule_id, class_id, room_id, study_date, time_slot, start_time, end_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, schedule_data)
            conn.commit()
            conn.close()
            return schedule_data[0]
        except Exception:
            return None

    @staticmethod
    def insert_schedules(schedule_list) -> bool:
        """Insert multiple schedules. Each schedule = (schedule_id, class_id, room_id, study_date, time_slot, start_time, end_time)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            for schedule in schedule_list:
                cursor.execute("""
                    INSERT INTO Schedule (schedule_id, class_id, room_id, study_date, time_slot, start_time, end_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, schedule)
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def delete_schedule_item(class_id, weekday, shift) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Schedule 
                WHERE class_id=? AND time_slot LIKE ?
            """, (class_id, f"%{weekday}%{shift}%"))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def get_student_count_by_class(class_id) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Class_Enrollment WHERE class_id = ?
        """, (class_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
