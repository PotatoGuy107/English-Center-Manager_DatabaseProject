"""Repository for Exam table operations"""
from infrastructure.config.database import get_connection


class ExamRepository:
    """Manages Exam records in SQL Server."""

    @staticmethod
    def get_all() -> list:
        """Get all exams with class info"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.exam_id, e.class_id, c.class_name, e.exam_type, e.exam_date, e.description
            FROM Exam e
            LEFT JOIN Class c ON e.class_id = c.class_id
            ORDER BY e.exam_date DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(exam_id) -> tuple:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT exam_id, class_id, exam_type, exam_date, description 
            FROM Exam WHERE exam_id=?
        """, (exam_id,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def get_by_class(class_id) -> list:
        """Get all exams for a class"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT exam_id, exam_type, exam_date, description 
            FROM Exam WHERE class_id=?
            ORDER BY exam_date
        """, (class_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(data) -> int:
        """Insert exam. data = (class_id, exam_type, exam_date, description). Returns exam_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Exam (class_id, exam_type, exam_date, description) 
            OUTPUT INSERTED.exam_id
            VALUES (?, ?, ?, ?)
        """, data)
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update(data) -> None:
        """Update exam. data = (exam_id, class_id, exam_type, exam_date, description)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Exam
            SET class_id=?, exam_type=?, exam_date=?, description=?
            WHERE exam_id=?
        """, (data[1], data[2], data[3], data[4], data[0]))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(exam_id) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Exam WHERE exam_id=?", (exam_id,))
        conn.commit()
        conn.close()
