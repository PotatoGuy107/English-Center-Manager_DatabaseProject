import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "quanlytrungtam.db")


class DashboardModel:

    @staticmethod
    def get_room_count():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Room")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_student_count():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Student")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_course_count():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Course")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_teacher_count():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Teacher")
        count = cursor.fetchone()[0]
        conn.close()
        return count
