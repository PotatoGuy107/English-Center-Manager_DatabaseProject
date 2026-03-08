import sqlite3

from domain.interfaces.i_course_repository import ICourseRepository
from infrastructure.config.database import DB_PATH


class CourseRepository(ICourseRepository):

    @staticmethod
    def get_all_courses() -> list:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name, level, fee, status FROM Course")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_skills_by_course(course_id) -> list:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT skill_name FROM Skill WHERE course_id = ?", (course_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_course(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Course VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update_course(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Course
            SET course_name=?, level=?, fee=?, status=?
            WHERE course_id=?
        """, (data[1], data[2], data[3], data[4], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_course(course_id) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Course WHERE course_id=?", (course_id,))
        conn.commit()
        conn.close()
