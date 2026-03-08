from infrastructure.config.database import get_connection


class DashboardRepository:

    @staticmethod
    def get_room_count() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Room")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_student_count() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Student")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_course_count() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Course")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def get_teacher_count() -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Teacher")
        count = cursor.fetchone()[0]
        conn.close()
        return count
