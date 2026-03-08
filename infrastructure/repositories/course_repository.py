from domain.interfaces.i_course_repository import ICourseRepository
from infrastructure.config.database import get_connection


class CourseRepository(ICourseRepository):

    @staticmethod
    def get_all_courses() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name, description, level, duration_weeks, tuition_fee, status FROM Course")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(course_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name, description, level, duration_weeks, tuition_fee, status FROM Course WHERE course_id=?", (course_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_skills_by_course(course_id) -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT skill_id, skill_name, description FROM Skill WHERE course_id = ?", (course_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_course(data) -> int:
        """Insert course. data = (course_name, description, level, duration_weeks, tuition_fee, status). Returns course_id (auto-generated)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Course (course_name, description, level, duration_weeks, tuition_fee, status) 
            OUTPUT INSERTED.course_id
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update_course(data) -> None:
        """Update course. data = (course_id, course_name, description, level, duration_weeks, tuition_fee, status)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Course
            SET course_name=?, description=?, level=?, duration_weeks=?, tuition_fee=?, status=?
            WHERE course_id=?
        """, (data[1], data[2], data[3], data[4], data[5], data[6], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_course(course_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Course WHERE course_id=?", (course_id,))
        conn.commit()
        conn.close()
