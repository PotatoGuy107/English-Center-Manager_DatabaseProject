"""Repository for Exam table operations"""
from infrastructure.config.database import get_connection


class ExamRepository:
    """Manages Exam records in SQL Server."""

    @staticmethod
    def get_next_exam_id() -> str:
        """Generate next exam_id like EX001, EX002, etc."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(exam_id, 3, LEN(exam_id)-2) AS INT)) FROM Exam WHERE exam_id LIKE 'EX%'")
        row = cursor.fetchone()
        conn.close()
        max_num = row[0] if row and row[0] else 0
        return f"EX{max_num + 1:03d}"

    @staticmethod
    def get_all() -> list:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.exam_id, e.class_id, e.exam_type, e.exam_date, e.description, c.class_name
            FROM Exam e
            LEFT JOIN Class c ON e.class_id = c.class_id
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
    def insert(data) -> str:
        """Insert exam. data = (exam_id, class_id, exam_type, exam_date, description). Returns exam_id."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Exam (exam_id, class_id, exam_type, exam_date, description) 
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        conn.close()
        return data[0]

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
