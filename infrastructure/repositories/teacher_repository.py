from domain.interfaces.i_teacher_repository import ITeacherRepository
from infrastructure.config.database import get_connection


class TeacherRepository(ITeacherRepository):

    @staticmethod
    def get_all() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id, full_name, phone_number, email, specialization, hire_date, status FROM Teacher")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(teacher_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT teacher_id, full_name, phone_number, email, specialization, hire_date, status FROM Teacher WHERE teacher_id=?", (teacher_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> int:
        """Insert teacher. data = (full_name, phone, email, specialization, hire_date, status). Returns teacher_id (auto-generated)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Teacher (full_name, phone_number, email, specialization, hire_date, status) 
            OUTPUT INSERTED.teacher_id
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update(data) -> None:
        """Update teacher. data = (teacher_id, full_name, phone, email, specialization, hire_date, status)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Teacher
            SET full_name=?, phone_number=?, email=?, specialization=?, hire_date=?, status=?
            WHERE teacher_id=?
        """, (data[1], data[2], data[3], data[4], data[5], data[6], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(teacher_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Teacher WHERE teacher_id=?", (teacher_id,))
        conn.commit()
        conn.close()
