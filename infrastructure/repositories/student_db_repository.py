import sqlite3

from infrastructure.config.database import DB_PATH


class StudentDbRepository:
    """Manages Student records in SQLite (used by admin user management screen)."""

    @staticmethod
    def get_all_students() -> list:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT student_id, full_name, phone_number, email, status FROM Student"
        )
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_student(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Student VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    @staticmethod
    def update_student(data) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student
            SET full_name=?, phone_number=?, email=?, status=?
            WHERE student_id=?
        """, (data[1], data[2], data[3], data[4], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_student(student_id) -> None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Student WHERE student_id=?", (student_id,))
        conn.commit()
        conn.close()
