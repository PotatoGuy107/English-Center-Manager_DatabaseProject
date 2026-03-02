import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "quanlytrungtam.db")


class KhoaHocModel:

    @staticmethod
    def get_all_courses():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name, level, fee, status FROM Course")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_skills_by_course(ma_kh):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT skill_name FROM Skill WHERE course_id = ?", (ma_kh,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def insert_course(data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Course VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update_course(data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Course 
            SET course_name=?, level=?, fee=?, status=? 
            WHERE course_id=?
        """, (data[1], data[2], data[3], data[4], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_course(course_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Course WHERE course_id = ?", (course_id,))
        conn.commit()
        conn.close()
